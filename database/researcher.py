from sqlalchemy import Column, Integer, String
from database.base import Base


class Researcher(Base):
    __tablename__ = "researcher"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_lattes_update = Column(String)  # TODO change to date?
    phd_college = Column(String)
    phd_defense_year = Column(Integer)
    google_scholar_id = Column(String)

    def __repr__(self):
        return str(self.__dict__)
