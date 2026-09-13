from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.user import User


with SessionLocal() as db:

    users = db.scalars(
        select(User)
    ).all()

    for user in users:
        print(
            f"{user.username:10} | "
            f"role={user.role.name:10} | "
            f"department={user.department.name:10} | "
            f"clearance={user.clearance_level}"
        )