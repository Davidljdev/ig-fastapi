# Instagram URL Manager – FastAPI

This small project provides both a **REST API** and an **HTML website** to manage Instagram URLs.
It allows users to **add, retrieve, and delete Instagram URLs** stored in a **SQLite database**, using **FastAPI** as the backend framework.

## Project Description (Short)

This project provides an API service and an HTML website to consume services related to adding, retrieving, and deleting Instagram URLs stored in a SQLite database.

## Python Virtual Environment (Python 3.11 – Fully Compatible)

### Create virtual environment
/opt/homebrew/bin/python3.11 -m venv venv

### (If you created it incorrectly and want to remove it)
deactivate  
rm -rf venv

### Activate virtual environment
source venv/bin/activate

## Install Dependencies

Install all required libraries inside the virtual environment:
pip install -r requirements.txt

Verify installed packages:
pip list

## Run the Application (Local Development)

Start the FastAPI server using Uvicorn:
uvicorn app.main:app --reload

API base URL: http://127.0.0.1:8000  
Swagger UI: http://127.0.0.1:8000/docs  
ReDoc: http://127.0.0.1:8000/redoc  

## Project Structure

ig-fastapi/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routes/
│   │   └── urls.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   └── js/
│
├── requirements.txt
└── urls.db
