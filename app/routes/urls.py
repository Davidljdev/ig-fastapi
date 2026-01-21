# app/routes/urls.py
from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import datetime, date, timezone
from sqlalchemy.orm import Session
from sqlalchemy import update
from app.db.database import SessionLocal
from app.db.models import Url
from app.schemas import UrlCreate
import re
from urllib.parse import urlparse

router = APIRouter(tags=["URLs"])

INSTAGRAM_REGEX = re.compile(
    r"^https?:\/\/(www\.)?instagram\.com\/.+",
    re.IGNORECASE
)

# -------------------
# Dependency
# -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------
# GET
# -------------------
@router.get("")
def get_urls(
    include_deleted: bool = False,
    url_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Url)
    if not include_deleted:
        query = query.filter(Url.deleted_at == None)
    if url_id is not None:
        query = query.filter(Url.id == url_id)

    urls = query.order_by(Url.created_at.desc()).all()
    return [
        {
            "id": u.id,
            "url": u.url,
            "created_at": u.created_at,
            "deleted_at": u.deleted_at
        }
        for u in urls
    ]

# -------------------
# PUT
# -------------------
@router.put("")
def add_url(payload: UrlCreate, db: Session = Depends(get_db)):
    url = str(payload.url)

    # Validación básica de esquema
    parsed = urlparse(url)
    if parsed.scheme not in ["http", "https"]:
        raise HTTPException(status_code=400, detail="Invalid URL scheme")
    
    # Validación que url no este vacía
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    # Validación con regex de Instagram
    if not INSTAGRAM_REGEX.match(url):
        raise HTTPException(status_code=400, detail={"message": "The URL does not correspond to Instagram."})

    # Verificar si ya existe
    existing = db.query(Url).filter(Url.url == url, Url.deleted_at == None).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail={
                "message": f"The URL has already been registered. [id: {existing.id}, created_at: {existing.created_at}]"
            }
        )

    now = datetime.now(timezone.utc)  # UTC
    new_url = Url(url=url, created_at=now)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {
        "detail": {
            "message": "URL added successfully",
            "url": url,
            "created_at": now.isoformat()
        }
    }

# -------------------
# DELETE (soft delete)
# -------------------
@router.delete("")
def delete_urls(
    delete_date: date = Query(..., description="Deletion date (YYYY-MM-DD)"),
    url_id: int | None = Query(None, description="URL ID (optional)"),
    db: Session = Depends(get_db)
):
    deleted_at = datetime.combine(delete_date, datetime.min.time()).replace(tzinfo=timezone.utc)

    query = db.query(Url).filter(Url.deleted_at == None)

    if url_id is not None:
        url_obj = query.filter(Url.id == url_id).first()
        if not url_obj:
            raise HTTPException(status_code=404, detail="URL not found or already deleted")
        url_obj.deleted_at = deleted_at
    else:
        # Soft delete masivo con update para eficiencia
        query.update({Url.deleted_at: deleted_at}, synchronize_session=False)

    db.commit()
    return {"message": "Deletion date applied successfully"}
