from dataclasses import dataclass, field
from typing import List

@dataclass
class Settings:
    credentials_file: str = "token.json"
    scopes: List[str] = field(default_factory=lambda: [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    default_spreadsheet_name: str = "API"
    edt_sheet_index: int = 1
