import os
from src.persistence.repository import Repository
from utils.constants import REPOSITORY_ENV_VAR
from src import db as sql_instance
from src.models.base import Base
from src.models.country import Country

db: Repository

if os.getenv(REPOSITORY_ENV_VAR) == "db":
    from src.persistence.db import DBRepository

    Base.metadata.create_all(sql_instance.engine)
    Country.metadata.create_all(sql_instance.engine)
    db = DBRepository()
elif os.getenv(REPOSITORY_ENV_VAR) == "file":
    from src.persistence.file import FileRepository

    print("Using file repository")

    db = FileRepository()
else:
    from src.persistence.memory import MemoryRepository

    db = MemoryRepository()
