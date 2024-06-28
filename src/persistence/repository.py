from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def reload(self): ...

    @abstractmethod
    def get_all(self, model_name: str) -> list: ...

    @abstractmethod
    def get(self, model_name: str, id: str): ...

    @abstractmethod
    def save(self, obj): ...

    @abstractmethod
    def update(self, obj): ...

    @abstractmethod
    def delete(self, obj) -> bool: ...
