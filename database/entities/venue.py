import enum

from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from config import QualisLevel
from database.base import Base


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
    papers = relationship('ConferencePaper', back_populates='venue')
    acronym = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "conference"
    }

    def __repr__(self):
        return str(self.__dict__)


class Journal(Venue):
    __tablename__ = "journal"

    id = Column(Integer, ForeignKey("venue.id"), primary_key=True)
    papers = relationship('JournalPaper', back_populates='venue')
    issn = Column(String)
    jcr = Column(Float)

    __mapper_args__ = {
        "polymorphic_identity": "journal"
    }

    def __repr__(self):
        return str(self.__dict__)
