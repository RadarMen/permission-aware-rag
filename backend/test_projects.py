from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.user import User


with SessionLocal() as db:

    users = db.scalars(
        select(User)
    ).all()

    for user in users:

        project_names = [
            project.name
            for project in user.projects
        ]

        print(
            f"{user.username:10} | "
            f"projects={project_names}"
        )