from datetime import datetime
from src.models.base import Base
from src.persistence.repository import Repository
from utils.populate import populate_db


class MemoryRepository(Repository):
    __data: dict[str, list] = {
        "country": [],
        "user": [],
        "amenity": [],
        "city": [],
        "review": [],
        "place": [],
        "placeamenity": [],
    }

    def __init__(self) -> None:
        self.reload()

    def get_all(self, model_name: str) -> list:
        return self.__data.get(model_name, [])

    def get(self, model_name: str, obj_id: str):
        for obj in self.get_all(model_name):
            if obj.id == obj_id:
                return obj
        return None

    def reload(self):
        populate_db(self)

    def save(self, obj: Base):
        cls = obj.__class__.__name__.lower()

        if obj not in self.__data[cls]:
            # print(f"Saving {obj}, {cls}")
            self.__data[cls].append(obj)

        return obj

    def update(self, obj: Base):
        cls = obj.__class__.__name__.lower()

        for i, o in enumerate(self.__data[cls]):
            if o.id == obj.id:
                obj.updated_at = datetime.now()
                self.__data[cls][i] = obj
                return obj

        return None

    def delete(self, obj: Base) -> bool:
        cls = obj.__class__.__name__.lower()

        if obj in self.__data[cls]:
            self.__data[cls].remove(obj)
            return True

        return False
