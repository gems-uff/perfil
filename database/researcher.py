from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database.base import Base


class Researcher(Base):
    __tablename__ = "researcher"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_lattes_update = Column(String)
    phd_college = Column(String)
    phd_defense_year = Column(Integer)
    google_scholar_id = Column(String)
    lattes_id = Column(Integer)

    def __repr__(self):
        return str(self.__dict__)


class Affiliation(Base):
    __tablename__ = "affiliation"

    researcher = Column(Integer, ForeignKey("researcher.id"), primary_key=True)
    year = Column(Integer, primary_key=True)

    def __repr__(self):
        return str(self.__dict__)
