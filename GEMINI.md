# CNUM - ENSAT Timetable Manager (Refactored)

CNUM est un outil Python conçu pour automatiser l'extraction, le nettoyage et l'analyse des emplois du temps de l'ENSAT à partir de Google Sheets. Le projet a été refondu selon une **Architecture Hexagonale** pour garantir modularité, testabilité et maintenabilité.

## 🛠 Aperçu du Projet

- **Objectif** : Automatiser la gestion des EDT, le calcul des heures d'enseignement et la synchronisation des calendriers.
- **Technologies** : Python 3.12+, `uv`, `gspread`, `pandas`, `icalendar`.

## 🏗 Architecture Hexagonale

Le projet est structuré pour isoler la logique métier des détails techniques :

### 1. Domaine (`src/domain/`)
Le cœur du projet, sans dépendance externe.
- `models.py` : Définition des objets `Session` et `Timetable` (DataClasses).
- `stats.py` : `StatsService` pour les calculs d'heures (Global, Hebdo, par Prof).
- `ports.py` : Interfaces (`TimetableRepository`, `TimetableRenderer`) définissant comment le domaine interagit avec l'extérieur.

### 2. Adaptateurs (`src/adapters/`)
Implémentations techniques des ports.
- **GSheet** (`gsheet/`) :
  - `client.py` : Client centralisé gérant l'authentification Google API.
  - `parser.py` : Extraction de l'EDT depuis Google Sheets (implémente `TimetableRepository`).
  - `drawer.py` : Rendu visuel et correctifs de fusion sur Google Sheets (implémente `TimetableRenderer`).
- **FS** (`fs/`) : Adaptateurs pour le système de fichiers (ex: CSV).

### 3. Configuration (`src/config_loader/`)
- `settings.py` : Gestion centralisée de la configuration via la classe `Settings` (Credentials, IDs de feuilles, Scopes).

### 4. Utilitaires (`src/utils/`)
- `functions.py` : Fonctions bas niveau pour le parsing de texte, calcul de coordonnées et extraction RGB.
- `fetch_data.py` : Helpers pour récupérer les dictionnaires de correspondance (noms, groupes).

## 🚀 Utilisation

### Installation
```bash
uv sync
```

### Exécution du workflow principal
Le point d'entrée unique est maintenant `app.py` :
```bash
uv run app.py
```
Ce script :
1. Charge la configuration.
2. Initialise le client GSheet.
3. Extrait les données (Parser).
4. Calcule les statistiques (StatsService).
5. Met à jour l'EDT visuel sur l'onglet `drawing` (Drawer).

## 📏 Conventions et Points Clés

- **Gestion des fusions** : Le `GSheetDrawer` inclut un algorithme de nettoyage dynamique qui supprime les fusions existantes dans la zone cible avant d'en créer de nouvelles, évitant les erreurs `APIError 400`.
- **Injection de dépendances** : Les adaptateurs reçoivent le client GSheet et la configuration par leurs constructeurs, facilitant le remplacement par des mocks pour les tests.
- **Nettoyage des données** : Le parsing des noms de professeurs et des types de cours est centralisé dans `src/utils/functions.py` via des expressions régulières robustes.

## 📂 Structure des Dossiers
```text
src/
├── domain/          # Logique métier pure
├── adapters/        # Implémentations (GSheet, CSV, etc.)
├── config_loader/   # Configuration et Settings
└── utils/           # Fonctions utilitaires partagées
app.py               # Orchestrateur (Point d'entrée)
```
