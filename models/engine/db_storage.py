#!/usr/bin/python3
"""Module for DBStorage class."""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Handles database storage using SQLAlchemy."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage engine and session."""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST", "localhost")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db}",
            pool_pre_ping=True
        )

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on current database session all objects depending on cls."""
        obj_dict = {}
        classes = {
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }
        if cls is not None:
            if isinstance(cls, str):
                cls = classes.get(cls, cls)
            try:
                for obj in self.__session.query(cls).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    obj_dict[key] = obj
            except Exception:
                pass
        else:
            for cl in classes.values():
                try:
                    for obj in self.__session.query(cl).all():
                        key = f"{obj.__class__.__name__}.{obj.id}"
                        obj_dict[key] = obj
                except Exception:
                    pass
        return obj_dict

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize the session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """Call remove() on the private session attribute (__session)."""
        self.__session.remove()
