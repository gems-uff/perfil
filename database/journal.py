from sqlalchemy import Column, Integer, String, Float
from database.base import Base


class Journal(Base):
    __tablename__ = "journal"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    issn = Column(String)
    qualis = Column(String) #TODO new rules
    jcr = Column(Float)

    def __repr__(self):
        return str(self.__dict__)
