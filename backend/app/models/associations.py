# 用于处理user和project之间的多对多关系

from sqlalchemy import Column, ForeignKey, Table

from app.db.base import Base


user_projects = Table(
    "user_projects",
    Base.metadata,

    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "project_id",
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True
    ),
)