from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, date
from src.db.database import get_connection
from src.schemas import UrlCreate
import re

#router = APIRouter(prefix="/urls", tags=["URLs"])
router = APIRouter(tags=["URLs"])

INSTAGRAM_REGEX = re.compile(
    r"^https?:\/\/(www\.)?instagram\.com\/.+",
    re.IGNORECASE
)

# -------------------
# GET
# -------------------
@router.get("")
def get_urls(
    include_deleted: bool = False,
    url_id: int | None = None
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, url, created_at, deleted_at
        FROM urls
        WHERE 1=1
    """
    params = []

    if not include_deleted:
        query += " AND deleted_at IS NULL"

    if url_id is not None:
        query += " AND id = ?"
        params.append(url_id)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    #return rows
    return [
        {
            "id": row["id"],
            "url": row["url"],
            "created_at": row["created_at"],
            "deleted_at": row["deleted_at"]
        }
        for row in rows
    ]


# -------------------
# PUT
# -------------------
@router.put("")
def add_url(payload: UrlCreate):
    url = str(payload.url)

    if not INSTAGRAM_REGEX.match(url):
        raise HTTPException(
            status_code=400,
            detail={
                "message": "The URL does not correspond to Instagram."
            }
        )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, created_at
        FROM urls
        WHERE url = ? AND deleted_at IS NULL
    """, (url,))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        raise HTTPException(
            status_code=409,
            detail={
                "message": "The URL has already been registered. [id: {id}, created_at: {created_at}]".format(
                    id=existing[0],
                    created_at=existing[1]
                )
            }
        )

    now = datetime.now()

    cursor.execute("""
        INSERT INTO urls (url, created_at)
        VALUES (?, ?)
    """, (url, now))

    conn.commit()
    conn.close()

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
    url_id: int | None = Query(None, description="URL ID (optional)")
):
    conn = get_connection()
    cursor = conn.cursor()

    deleted_at = datetime.combine(delete_date, datetime.min.time())

    if url_id is not None:
        cursor.execute("""
            UPDATE urls
            SET deleted_at = ?
            WHERE id = ? AND deleted_at IS NULL
        """, (deleted_at, url_id))

        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(
                status_code=404,
                detail="URL not found or already deleted"
            )

    else:
        cursor.execute("""
            UPDATE urls
            SET deleted_at = ?
            WHERE deleted_at IS NULL
        """, (deleted_at,))

    conn.commit()
    conn.close()

    return {"message": "Deletion date applied successfully"}
