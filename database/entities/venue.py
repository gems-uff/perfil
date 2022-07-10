import enum

from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum
from database.base import Base


class QualisLevel(enum.Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    B3 = "B3"
    B4 = "B4"
    B5 = "B5"
    C = "C"
    NC = "NC"


class Venue(Base):
    __tablename__ = "venue"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    qualis = Column(Enum(QualisLevel))
    official_forum = Column(String)
    type = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "venue",
        "polymorphic_on": type
    }

    def __repr__(self):
        return str(self.__dict__)


class Conference(Venue):
    __tablename__ = "conference"

    id = Column(Integer, ForeignKey("venue.id"), primary_key=True)
    acronym = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "conference"
    }

    def __repr__(self):
        return str(self.__dict__)


class Journal(Venue):
    __tablename__ = "journal"

    id = Column(Integer, ForeignKey("venue.id"), primary_key=True)
    issn = Column(String)
    jcr = Column(Float)

    __mapper_args__ = {
        "polymorphic_identity": "journal"
    }

    def __repr__(self):
        return str(self.__dict__)
