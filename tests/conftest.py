import pytest
from config import settings
from scripts.seed_data import cargar

@pytest.fixture(autouse=True)
def base_aislada(tmp_path, monkeypatch):
    path=tmp_path/'pruebas.db'
    monkeypatch.setattr(settings,'DB_PATH',path)
    cargar(path)
