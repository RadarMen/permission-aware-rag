from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User

class Department(Base):
    __tablename__ = "departments"
    # 告诉 SQLAlchemy 这是一个映射类，映射到数据库中的表
    # 声明 id 列，类型为 int，是主键，自动递增
    id: Mapped[int] = mapped_column(
    # 这个id:Mapped[int] 表示这是一个映射的列，类型为整数
        primary_key = True,
        autoincrement = True,
    )
    # 声明 name 列，类型为 str，长度为 50，唯一且不为空
    name: Mapped[str] = mapped_column(
        String(50),
        unique = True,  # name 列的值必须唯一
        nullable = False, # name 列不能为空
    )

    users: Mapped[list["User"]] = relationship(
        back_populates = "department",
    )