from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.department import Department
    from app.models.project import Project
    from app.models.user import User


class DocumentVisibility(str, Enum):
    PUBLIC = "public"
    DEPARTMENT = "department"
    PROJECT = "project"
    PRIVATE = "private"

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    visibility: Mapped[DocumentVisibility] = mapped_column(
        SQLEnum(DocumentVisibility),
        nullable=False
    )

    classification_level: Mapped[int] = mapped_column(
        nullable=False,
        default=1
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    department_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id"),
        nullable=True
    )

    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    owner: Mapped["User"] = relationship(
        back_populates="owned_documents"
    )

    department: Mapped["Department | None"] = relationship(
        back_populates="documents"
    )

    project: Mapped["Project | None"] = relationship(
        back_populates="documents"
    )