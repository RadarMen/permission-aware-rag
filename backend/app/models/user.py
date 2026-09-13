from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.associations import user_projects

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.department import Department
    from app.models.project import Project

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), # 数据库外键，关联到roles表的id字段
        nullable=False
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"), # 数据库外键，关联到departments表
        nullable=False
    )

    clearance_level: Mapped[int] = mapped_column(
        default = 1,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    role: Mapped["Role"] = relationship(
        # 上面的role_id是真正存入数据库的
        # 这里的role是SQLAlchemy帮我们建立的对象关系，以后可以直接通过user.role.name来得到角色名称
        back_populates="users" # 不仅可以通过user.role来访问角色对象，还可以通过role.users来访问所有属于该角色的用户列表
    )

    department: Mapped["Department"] = relationship(
        # 和role同理。
        back_populates="users" 
    )

    projects: Mapped[list["Project"]] = relationship(
        secondary=user_projects,
        back_populates="members"
    )