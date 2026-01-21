from pydantic import BaseModel, HttpUrl

class UrlCreate(BaseModel):
    url: HttpUrl
