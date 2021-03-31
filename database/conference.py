from sqlalchemy import Column, Integer, String
from database.base import Base


class Conference(Base):
    __tablename__ = "conference"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    acronym = Column(String)
    qualis = Column(String) #TODO new rules
    h5 = Column(String)

    def __repr__(self):
        return str(self.__dict__)
