"""
该脚本用于初始化数据库，创建一些默认的部门、角色和用户。
建立一套固定测试环境。
"""

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.department import Department
from app.models.role import Role
from app.models.user import User
from app.models.project import Project

from app.models.document import Document, DocumentVisibility

def seed_db():
    with SessionLocal() as db:

        # =========================
        # 1. Departments
        # =========================

        department_names = [
            "R&D",
            "Finance",
            "HR",
            "IT",
        ]

        departments = {}

        for name in department_names:
            department = db.scalar(
                select(Department).where(
                    Department.name == name
                )
            )

            if department is None:
                department = Department(name=name)
                db.add(department)
                db.flush()

                print(f"Created department: {name}")

            departments[name] = department


        # =========================
        # 2. Roles
        # =========================

        role_data = {
            "employee": "Normal employee",
            "manager": "Department or project manager",
            "admin": "System administrator",
        }

        roles = {}

        for name, description in role_data.items():
            role = db.scalar(
                select(Role).where(
                    Role.name == name
                )
            )

            if role is None:
                role = Role(
                    name=name,
                    description=description
                )

                db.add(role)
                db.flush()

                print(f"Created role: {name}")

            roles[name] = role


        # =========================
        # 3. Users
        # =========================

        user_data = [
            {
                "username": "alice",
                "email": "alice@example.com",
                "department": "R&D",
                "role": "employee",
                "clearance_level": 1,
            },
            {
                "username": "bob",
                "email": "bob@example.com",
                "department": "R&D",
                "role": "manager",
                "clearance_level": 3,
            },
            {
                "username": "carol",
                "email": "carol@example.com",
                "department": "Finance",
                "role": "employee",
                "clearance_level": 2,
            },
            {
                "username": "admin",
                "email": "admin@example.com",
                "department": "IT",
                "role": "admin",
                "clearance_level": 5,
            },
        ]

        for data in user_data:

            user = db.scalar(
                select(User).where(
                    User.username == data["username"]
                )
            )

            if user is not None:
                continue

            user = User(
                username=data["username"],
                email=data["email"],

                # Authentication 还没做。
                # 这不是密码，只是暂时满足 NOT NULL。
                password_hash="NOT_CONFIGURED_YET",

                department=departments[
                    data["department"]
                ],

                role=roles[
                    data["role"]
                ],

                clearance_level=data[
                    "clearance_level"
                ],
            )

            db.add(user)

            print(
                f"Created user: "
                f"{data['username']}"
            )

        # =========================
        # 4. Projects
        # =========================

        project_data = [
            {
                "name": "Apollo",
                "description": "Next-generation R&D platform",
                "department": "R&D",
            },
            {
                "name": "Gemini",
                "description": "Experimental AI research project",
                "department": "R&D",
            },
            {
                "name": "FinanceCore",
                "description": "Internal finance modernization project",
                "department": "Finance",
            },
        ]

        projects = {}

        for data in project_data:

            project = db.scalar(
                select(Project).where(
                    Project.name == data["name"]
                )
            )

            if project is None:
                project = Project(
                    name=data["name"],
                    description=data["description"],
                    department=departments[
                        data["department"]
                    ]
                )

                db.add(project)
                db.flush()

                print(
                    f"Created project: "
                    f"{data['name']}"
                )

            projects[data["name"]] = project
        # =========================
        # 5. Project Memberships
        # =========================

        membership_data = {
            "alice": [
                "Apollo",
            ],

            "bob": [
                "Apollo",
                "Gemini",
            ],

            "carol": [
                "FinanceCore",
            ],

            "admin": [],
        }
        for username, project_names in membership_data.items():

            user = db.scalar(
                select(User).where(
                    User.username == username
                )
            )

            for project_name in project_names:

                project = projects[project_name]

                if project not in user.projects:
                    user.projects.append(project)

                    print(
                        f"Added {username} "
                        f"to {project_name}"
                    )

        # =========================
        # 6. Documents
        # =========================

        document_data = [
            {
                "title": "Employee Handbook",
                "visibility": DocumentVisibility.PUBLIC,
                "classification_level": 1,
                "owner": "admin",
                "department": None,
                "project": None,
            },

            {
                "title": "R&D Internal Guidelines",
                "visibility": DocumentVisibility.DEPARTMENT,
                "classification_level": 1,
                "owner": "bob",
                "department": "R&D",
                "project": None,
            },

            {
                "title": "Apollo Architecture",
                "visibility": DocumentVisibility.PROJECT,
                "classification_level": 2,
                "owner": "bob",
                "department": "R&D",
                "project": "Apollo",
            },

            {
                "title": "Apollo Secret Roadmap",
                "visibility": DocumentVisibility.PROJECT,
                "classification_level": 3,
                "owner": "bob",
                "department": "R&D",
                "project": "Apollo",
            },

            {
                "title": "Finance Budget",
                "visibility": DocumentVisibility.DEPARTMENT,
                "classification_level": 2,
                "owner": "carol",
                "department": "Finance",
                "project": None,
            },

            {
                "title": "Bob Private Notes",
                "visibility": DocumentVisibility.PRIVATE,
                "classification_level": 1,
                "owner": "bob",
                "department": None,
                "project": None,
            },
        ]
        
        for data in document_data:

            document = db.scalar(
                select(Document).where(
                    Document.title == data["title"]
                )
            )

            if document is not None:
                continue

            owner = db.scalar(
                select(User).where(
                    User.username == data["owner"]
                )
            )

            department = (
                departments[data["department"]]
                if data["department"] is not None
                else None
            )

            project = (
                projects[data["project"]]
                if data["project"] is not None
                else None
            )

            document = Document(
                title=data["title"],
                visibility=data["visibility"],
                classification_level=data["classification_level"],
                owner=owner,
                department=department,
                project=project,
            )

            db.add(document)

            print(
                f"Created document: "
                f"{data['title']}"
            )

        db.commit()

        print("Database seed completed.")


if __name__ == "__main__":
    seed_db()