from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_schemadisplay import create_schema_graph

from database.base import Base
from database.entities.venue import Venue, Conference, Journal
from database.entities.titles_support import ResearcherAdvisement, ResearcherCommittee
from database.entities.project import Project, ResearcherProject
from database.entities.researcher import Researcher, Affiliation
from database.entities.paper import Paper, JournalPaper, ConferencePaper, journal_association_table, conference_association_table
from database.entities.book import BookManuscript, Book, BookChapter, ResearcherPublishedBook, ResearcherPublishedBookChapter
from database.entities.other_works import Patent, ResearcherEditorialBoard, ResearcherConferenceManagement, ResearcherPatent


def start_database(sqlite: bool):
    """Starts the database returning the session"""
    engine = create_engine("sqlite:///:memory:", echo=False)
    if sqlite:
        engine = create_engine("sqlite:///db.sqlite3", echo=False)

    Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    SessionObject = Session()
    return SessionObject


def database_schema_png():
    """Creates and .png with a schema of the database"""
    # remember to change the engine to one which is persistent
    Session = start_database(True)
    graph = create_schema_graph(metadata=MetaData("sqlite:///db.sqlite3"),
                                show_datatypes=False,  # The image would get nasty big if we"d show the datatypes
                                show_indexes=False,  # ditto for indexes
                                rankdir="LR",  # From left to right (instead of top to bottom)
                                concentrate=False  # Don"t try to join the relation lines together
                                )
    graph.write_png("dbschema.png")  # write out the file
