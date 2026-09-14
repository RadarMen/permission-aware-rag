from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.associations import user_projects

if TYPE_CHECKING:
    from app.models.department import Department
    from app.models.user import User
    from app.models.document import Document


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
        nullable=False
    )

    department: Mapped["Department"] = relationship(
        back_populates="projects"
    )

    members: Mapped[list["User"]] = relationship(
        secondary=user_projects,
        back_populates="projects"
    )

    documents: Mapped[list["Document"]] = relationship(
        back_populates="project"
    )