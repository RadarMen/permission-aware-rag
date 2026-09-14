from app.models.document import Document, DocumentVisibility
from app.models.user import User


def can_access_document(
    user: User,
    document: Document
) -> bool:

    # 1. 被禁用用户没有任何访问权限
    if not user.is_active:
        return False

    # 2. Admin 全局放行
    if user.role.name == "admin":
        return True

    # 3. Clearance 是所有普通文档访问的基本门槛
    if user.clearance_level < document.classification_level:
        return False

    # 4. Internal public
    if document.visibility == DocumentVisibility.PUBLIC:
        return True

    # 5. Department-only
    if document.visibility == DocumentVisibility.DEPARTMENT:
        return (
            document.department_id is not None
            and user.department_id == document.department_id
        )

    # 6. Project-only
    if document.visibility == DocumentVisibility.PROJECT:

        if document.project_id is None:
            return False

        # 先要求同部门
        if user.department_id != document.department_id:
            return False

        user_project_ids = {
            project.id
            for project in user.projects
        }

        return document.project_id in user_project_ids

    # 7. Private
    if document.visibility == DocumentVisibility.PRIVATE:
        return document.owner_id == user.id

    # Fail closed
    return False