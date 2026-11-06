import os
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
DATA_DIR = BASE_DIR / 'data'
DB_PATH = Path(os.getenv('DB_PATH', str(DATA_DIR / 'servicedesk.db')))
CHROMA_DIR = DATA_DIR / 'chroma_db'
DEMO_DATE = date.fromisoformat(os.getenv('DEMO_DATE', '2025-10-15'))
UMBRAL_APROBACION = 100_000
UMBRAL_PREFERENTE = 50_000
UMBRAL_RECURRENCIA = 3
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
LLM_MODEL = os.getenv('LLM_MODEL', 'gemini-3.5-flash')
os.environ.setdefault('ANONYMIZED_TELEMETRY', 'False')
os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY', '1')
