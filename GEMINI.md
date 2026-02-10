# CNUM - ENSAT Timetable Manager

CNUM is a Python-based tool designed to automate the extraction, cleaning, and analysis of ENSAT (École Nationale Supérieure Agronomique de Toulouse) timetables from Google Sheets. It transforms complex spreadsheet data into structured formats for teaching hour tracking and digital calendar integration.

## 🛠 Project Overview

- **Purpose**: Automate timetable management, teacher hour calculations, and calendar synchronization.
- **Main Technologies**: 
    - **Language**: Python 3.12+
    - **Dependency Management**: [uv](https://github.com/astral-sh/uv)
    - **Google Sheets API**: `gspread`, `gspread-dataframe`, `gspread-formatting`
    - **Data Processing**: `pandas`
    - **Visualization**: `plotly`
    - **Calendar Export**: `icalendar`

## 🏗 Architecture

The project is structured as follows:

- `src/scripts/`: Primary scripts for core tasks.
    - `parse_edt.py`: Extracts raw data from Google Sheets, handles merged cells, and normalizes teacher names.
    - `ical_conversion.py`: Converts parsed data into `.ics` format.
    - `draw_df.py`: Generates visualizations for statistics.
- `src/calcul/`: Statistical logic.
    - `calculate_stat_df.py`: Functions to compute hour totals per teacher and course type.
- `src/main_functions/`: Orchestration and sheet building.
    - `build_sheets.py`: Logic to generate individual teacher sheets in Google Sheets.
- `src/utils/`: Low-level utilities.
    - `functions.py`, `dummies.py`, `fetch_data.py`: Helpers for data fetching, string parsing, and cell coordinate mapping.
- `src/config.py`: Centralized configuration for Google API scopes, credentials, and sheet indices.

## 🚀 Building and Running

### Setup
Ensure you have `uv` installed.
```bash
uv sync
```

### Configuration
1. Place a Google Cloud Service Account credentials file named `token.json` in the project root.
2. Update `src/config.py` with the correct spreadsheet indices if necessary.

### Key Commands
- **Full Workflow**: `uv run demo.py` (Parses, visualizes, and builds a teacher sheet).
- **Parse Timetable**: `uv run src/scripts/parse_edt.py` (Generates `finale.csv` and updates Google Sheets).
- **Export to iCal**: `uv run src/scripts/ical_conversion.py` (Generates `mon_edt.ics`).
- **Visualize Stats**: `uv run src/scripts/draw_df.py`.
- **Run Tests**: `uv run pytest`.

## 📏 Development Conventions

- **Data Integrity**: Parsing relies heavily on `get_all_merges` to correctly attribute hours to merged cells in the source sheets.
- **Naming Normalization**: Teacher initials (e.g., "ML", "BP") are mapped to full names (e.g., "Marc Lang", "Benjamin Pey") via `corr_names` in `parse_edt.py`.
- **Intermediary Data**: `finale.csv` serves as the primary local data source after parsing.
- **Testing**: Tests are located in `tests/` and `src/tests/`, focusing on extraction accuracy and statistical calculations.
