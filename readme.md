
# crear entorno virtual para python 3.11 (compatible total)
/opt/homebrew/bin/python3.11 -m venv venv

## si lo creaste mal y quieres eliminarlo
deactivate
rm -rf venv

# activar entorno
source venv/bin/activate
# instalar librerias en entorno
pip install -r requirements.txt
# ver que librerias se instalaron bien
pip list
# ejecutar servicio
uvicorn app.main:app --reload




# estructura del proyecto fastapi
ig-fastapi/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routes/
│   │   └── urls.py
│
├── templates/        ← HTML (la web)
│   └── index.html
│
├── static/           ← CSS / JS
│   ├── css/
│   └── js/
│
├── requirements.txt
└── urls.db


