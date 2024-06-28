"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""

from src.models.base import Base
from src.persistence.repository import Repository
from src import db
from src.models.amenity import Amenity, PlaceAmenity
from src.models.city import City
from src.models.country import Country
from src.models.place import Place
from src.models.review import Review
from src.models.user import User
from utils.populate import populate_db


class DBRepository(Repository):
    def __init__(self) -> None:
        self.models = {
            "city": City,
            "country": Country,
            "place": Place,
            "placeamenity": PlaceAmenity,
            "amenity": Amenity,
            "user": User,
            "review": Review,
        }
        self.reload()

    def get_all(self, model_name: str) -> list:
        return self.models.get(model_name.lower()).query.all()

    def get(self, model_name: str, obj_id: str):
        return self.models.get(model_name.lower()).query.get(obj_id)

    def reload(self):
        populate_db(self)

    def save(self, obj: Base):
        db.session.add(obj)
        db.session.commit()

    def update(self, obj: Base):
        # Étape 1 : Récupérer l'objet
        model = self.get(type(obj).__name__, obj.id)
        if not model:
            return None  # L'objet n'a pas été trouvé

        # Étape 2 : Modifier les attributs
        for key, value in obj.__dict__.items():
            setattr(model, key, value)

        # Étape 3 : Ajouter l'objet modifié à la session
        db.session.add(model)

        # Étape 4 : Valider la session
        try:
            db.session.commit()
            return obj
        except Exception:
            db.session.rollback()  # Annuler les modifications en cas d'erreur
            return None

    def delete(self, obj: Base) -> bool:
        try:
            db.session.delete(obj)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()  # Annule les modifications en cas d'erreur
            return False
