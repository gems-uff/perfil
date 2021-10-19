import enum
from sqlalchemy import Column, Integer, String,Table, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database.base import Base

journal_association_table = Table("researcher_journal_paper", Base.metadata,
                                  Column("researcher_id", Integer, ForeignKey("researcher.id")),
                                  Column("journal_paper_id", Integer, ForeignKey("journal_paper.id")))

conference_association_table = Table("researcher_conference_paper", Base.metadata,
                                     Column("researcher_id", Integer, ForeignKey("researcher.id")),
                                     Column("conference_paper_id", Integer, ForeignKey("conference_paper.id")))


class PaperNature(enum.Enum):
    COMPLETE = "artigo completo"
    ABSTRACT = "resumo"
    EXPANDED_ABSTRACT = "resumo expandido"


class Paper(Base):
    __tablename__ = "paper"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    nature = Column(Enum(PaperNature))
    year = Column(Integer)
    doi = Column(String)
    first_page = Column(Integer)
    last_page = Column(Integer)
    authors = Column(String)
    type = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "paper",
        "polymorphic_on": type
    }

    def __repr__(self):
        return str(self.__dict__)


class JournalPaper(Paper):
    __tablename__ = "journal_paper"

    id = Column(Integer, ForeignKey("paper.id"), primary_key=True)
    venue = Column(Integer, ForeignKey("journal.id"))
    researchers = relationship("Researcher", secondary=journal_association_table, backref="journal_papers")

    __mapper_args__ = {
        "polymorphic_identity": "journal_paper"
    }

    def __repr__(self):
        return str(self.__dict__)


class ConferencePaper(Paper):
    __tablename__ = "conference_paper"

    id = Column(Integer, ForeignKey("paper.id"), primary_key=True)
    venue = Column(Integer, ForeignKey("conference.id"))
    researchers = relationship("Researcher", secondary=conference_association_table, backref="conference_papers")

    __mapper_args__ = {
        "polymorphic_identity": "conference_paper"
    }

    def __repr__(self):
        return str(self.__dict__)
