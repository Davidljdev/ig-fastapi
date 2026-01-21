# test_db.py
import os
from sqlalchemy import create_engine, text  # <-- IMPORTAR text

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("No se encontró DATABASE_URL en tu .env")

# Crear engine
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM urls"))  # <-- usar text()
        print("✅ Conexión exitosa! Resultado:", result.fetchone())
except Exception as e:
    print("❌ Error de conexión:", e)
