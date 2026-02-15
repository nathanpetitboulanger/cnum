# CNUM - ENSAT Timetable Manager (Refactored)

CNUM est un outil Python conçu pour automatiser l'extraction, le nettoyage et l'analyse des emplois du temps de l'ENSAT à partir de Google Sheets. Le projet suit une **Architecture Hexagonale** garantissant modularité et maintenabilité.

## 🛠 Aperçu du Projet

- **Objectif** : Automatiser la gestion des EDT, le calcul des heures d'enseignement et la synchronisation visuelle.
- **Workflow Central** : `EDT (Brut)` ➔ `edt_clean (Tabulaire)` ➔ `drawing (Visuel)`.
- **Technologies** : Python 3.12+, `uv`, `gspread`, `pandas`.

## 🏗 Architecture Hexagonale

### 1. Domaine (`src/domain/`)
Logique métier pure, sans dépendances externes.
- `models.py` : Objets `Session` et `Timetable`.
- `stats.py` : `StatsService` pour les calculs d'heures par prof, semaine et type.
- `ports.py` : Interfaces (`TimetableRepository`, `TimetableRenderer`) définissant les contrats d'entrée/sortie.

### 2. Adaptateurs (`src/adapters/`)
Implémentations techniques des ports.
- **GSheet** (`gsheet/`) :
  - `client.py` : Client centralisé (Singleton) pour l'authentification Google API.
  - `parser.py` : Extraction de l'EDT complexe (fusions, couleurs).
  - `clean_parser.py` : Lecture du format tabulaire simplifié depuis `edt_clean`.
  - `exporter.py` : Synchronisation des données extraites vers `edt_clean`.
  - `drawer.py` : Rendu visuel complexe (fusions, couleurs, grisé pour les previews).

### 3. Configuration & Utils
- `config_loader/settings.py` : Gestion des credentials et IDs de feuilles via une classe `Settings`.
- `utils/functions.py` : Parsing regex, détection de fusions et conversion RGB.
- `utils/fetch_data.py` : Récupération des dictionnaires de correspondance (Initiales ➔ Noms).

## 🚀 Utilisation (Streamlit)

L'application est pilotée par `app.py` avec trois étapes clés :

1. **Extraction & Sync** : 
   - `Parser l'EDT Brut & Sync` : Extrait depuis l'onglet `EDT`, nettoie les titres, et remplit l'onglet `edt_clean`.
   - `Charger depuis 'edt_clean'` : Charge les données tabulaires (utile après modifications manuelles dans le tableur).
2. **Statistiques** : Calcul immédiat des totaux d'heures.
3. **Rendu Visuel** :
   - `Générer la feuille 'drawing'` : Crée un emploi du temps visuel complet.
   - `Prévisu Professeur` : Génère une feuille spécifique où seuls les cours de l'enseignant sélectionné sont colorés (le reste est grisé).

## 📏 Règles de Formatage et Conventions

- **Syntaxe des cellules** : Le dessin génère automatiquement le format : `Nom du Cours \n (INITIALES) [SALLE] "TYPE"`.
- **Gestion des conflits** : Le `GSheetDrawer` intègre une grille d'occupation cellule par cellule pour éviter toute erreur de chevauchement lors des fusions groupées.
- **Couleurs** : Les couleurs sont extraites dynamiquement et normalisées pour l'API Google (0-1).

## 📂 Structure des Dossiers
```text
src/
├── domain/          # Modèles et Logique de calcul
├── adapters/        # Adaptateurs GSheet (Parser, Drawer, Exporter)
├── config_loader/   # Configuration Settings
└── utils/           # Fonctions de parsing et helpers
app.py               # Orchestrateur Streamlit
```
