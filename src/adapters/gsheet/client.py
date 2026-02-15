import gspread
from oauth2client.service_account import ServiceAccountCredentials
from src.config_loader.settings import Settings

class GSheetClient:
    """Gestionnaire centralisé de la connexion à Google Sheets (Singleton-like)."""
    
    _instance = None
    
    def __new__(cls, settings: Settings):
        if cls._instance is None:
            cls._instance = super(GSheetClient, cls).__new__(cls)
            cls._instance._client = None
            cls._instance.settings = settings
        return cls._instance

    @property
    def client(self):
        if self._client is None:
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.settings.credentials_file, 
                self.settings.scopes
            )
            self._client = gspread.authorize(creds)
        return self._client

    def open_spreadsheet(self, name: str = None):
        name = name or self.settings.default_spreadsheet_name
        return self.client.open(name)
