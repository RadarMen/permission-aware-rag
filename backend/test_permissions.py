from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.document import Document
from app.models.user import User
from app.services.permission import can_access_document


with SessionLocal() as db:

    users = db.scalars(
        select(User)
    ).all()

    documents = db.scalars(
        select(Document)
    ).all()

    for user in users:

        print()
        print(f"===== {user.username.upper()} =====")

        for document in documents:

            allowed = can_access_document(
                user,
                document
            )

            status = (
                "ALLOW"
                if allowed
                else "DENY"
            )

            print(
                f"{status:5} | "
                f"{document.title}"
            )