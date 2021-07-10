from sqlalchemy import Boolean, Column, String, Integer
from app.models.base import BaseModel
from app.models.db_user_profile import DbUserProfile


class DbArticle(BaseModel):
    slug: Column(String, index=True, unique=True, nullable=False)
    title: Column(String)
    description: Column(String)
    body: Column(String)
    tags: Column(String)
    author: DbUserProfile
    favorited: Column(Boolean())
    favorites_count: Column(Integer)
