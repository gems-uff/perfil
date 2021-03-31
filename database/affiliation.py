from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database.base import Base


class Affiliation(Base):
    __tablename__ = "affiliation"

    researcher = Column(Integer, ForeignKey("researcher.id"), primary_key=True)
    year = Column(Integer, primary_key=True)

    def __repr__(self):
        return str(self.__dict__)
