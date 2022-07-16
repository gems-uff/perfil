import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from database.base import Base


class EditorialBoardType(enum.Enum):
    EDITORIAL_BOARD = "editorial_board"
    REVISER = "reviewer"


class EditorialBoard(Base):
    __tablename__ = "reseacher_editorial_board"

    id = Column(Integer, primary_key=True)
    researcher_id = Column(Integer, ForeignKey("researcher.id"))
    journal_name = Column(String)
    type = Column(Enum(EditorialBoardType))
    start_year = Column(Integer)
    end_year = Column(Integer)

    researchers = relationship("Researcher", backref="journal_editorial_boards")

    def __repr__(self):
        return str(self.__dict__)


class ConferenceOrganization(Base):
    __tablename__ = "researcher_conference_management"

    id = Column(Integer, primary_key=True)
    researcher_id = Column(Integer, ForeignKey("researcher.id"))
    title = Column(String) #the name of the job at the conference
    year = Column(Integer)
    committee = Column(String)


class PatentType(enum.Enum):
    PATENT = "patent"
    SOFTWARE = "computer_software"


class Patent(Base):
    __tablename__ = "patent"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(PatentType))
    title = Column(String)
    authors = Column(String)
    local_of_registry = Column(String)
    number = Column(String)
    year = Column(Integer)


class ResearcherPatent(Base):
    __tablename__ = "researcher_patent"

    patent_id = Column(Integer, ForeignKey('patent.id'), primary_key=True)
    researcher_id = Column(Integer, ForeignKey('researcher.id'), primary_key=True)

    def __repr__(self):
        return str(self.__dict__)