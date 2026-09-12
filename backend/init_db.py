# 临时初始化脚本
# 创建数据库和表

from app.db.base import Base
from app.db.session import engine

import app.models

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()