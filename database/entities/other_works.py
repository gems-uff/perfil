import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from database.base import Base


class EditorialBoardType(enum.Enum):
    EDITORIAL_BOARD = "editorial_board"
    REVISER = "reviewer"


class ResearcherEditorialBoard(Base):
    __tablename__ = "reseacher_editorial_board"

    researcher_id = Column(Integer, ForeignKey("researcher.id"), primary_key=True)
    journal_name = Column(String, primary_key=True)
    type = Column(Enum(EditorialBoardType), primary_key=True)
    start_year = Column(Integer, primary_key=True)
    end_year = Column(Integer)

    researchers = relationship("Researcher", backref="journal_editorial_boards")

    def __repr__(self):
        return str(self.__dict__)


class ResearcherConferenceManagement(Base):
    __tablename__ = "researcher_conference_management"

    researcher_id = Column(Integer, ForeignKey("researcher.id"), primary_key=True)
    title = Column(String, primary_key=True) #the name of the job at the conference
    year = Column(Integer, primary_key=True)
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

    researchers = relationship("Researcher", backref="patents")
    patents = relationship("Patent", backref="researchers")

    def __repr__(self):
        return str(self.__dict__)