# CNUM ENSAT - Gestionnaire d'Emploi du Temps

CNUM est un outil Python conçu pour automatiser l'extraction, le nettoyage et l'analyse des emplois du temps (EDT) de l'ENSAT à partir de Google Sheets. Il permet de transformer des feuilles de calcul complexes en données structurées pour le suivi des heures d'enseignement et l'intégration dans des calendriers numériques.

## 🚀 Fonctionnalités

- **Parsing Automatisé** : Extraction des données depuis Google Sheets, avec gestion intelligente des cellules fusionnées pour déterminer les durées exactes.
- **Nettoyage des Données** : Mapping automatique des initiales des professeurs vers leurs noms complets et normalisation des titres de cours.
- **Analyse Statistique** : Calcul automatique du volume horaire total par professeur et par type d'enseignement.
- **Génération de Vues Personnalisées** : Création automatique de feuilles de calcul spécifiques pour chaque enseignant.
- **Export iCal** : Conversion des données d'emploi du temps au format `.ics` pour une synchronisation facile avec Google Calendar, Outlook, ou Apple Calendar.
- **Visualisation** : Support pour la génération de graphiques de statistiques via Plotly.

## 🛠️ Installation

Ce projet utilise [uv](https://github.com/astral-sh/uv) pour la gestion des dépendances.

1. Clonez le dépôt :
   ```bash
   git clone <repository-url>
   cd cnum
   ```

2. Installez les dépendances :
   ```bash
   uv sync
   ```

## ⚙️ Configuration

1. **Accès API Google** : 
   - Placez votre fichier de credentials Google Cloud (Service Account) nommé `token.json` à la racine du projet.
   - Partagez votre Google Sheet avec l'adresse e-mail du compte de service.
2. **Paramètres** : 
   - Modifiez `src/config.py` pour ajuster l'index de la feuille (`edt_sheet_index`) à utiliser.

## 📖 Utilisation

### Extraction et Analyse
Pour lancer le processus complet (parsing, nettoyage et statistiques) :
```bash
uv run demo.py
```

### Scripts Individuels
- **Parsing** : `uv run src/scripts/parse_edt.py` (Génère `finale.csv`)
- **Conversion iCal** : `uv run src/scripts/ical_conversion.py` (Génère `mon_edt.ics`)
- **Visualisation** : `uv run src/scripts/draw_df.py`

## 📁 Structure du Projet

- `src/scripts/` : Scripts principaux pour le parsing et la conversion.
- `src/calcul/` : Logique de calcul des statistiques.
- `src/utils/` : Fonctions utilitaires pour l'interaction avec Google Sheets et la manipulation de données.
- `src/global_draw_functions/` : Fonctions de haut niveau pour la construction des feuilles.
- `tests/` : Suite de tests unitaires pour vérifier l'extraction et les calculs.

## 🧪 Tests

Lancez les tests avec `pytest` :
```bash
uv run pytest
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à proposer une pull request.

## 📄 Licence

Ce projet est sous licence MIT.