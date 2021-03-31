from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_schemadisplay import create_schema_graph

from database.base import Base
from database.conference import Conference
from database.student import Student, ResearcherStudent
from database.journal import Journal
from database.project import Project, ResearcherProject
from database.researcher import Researcher
from database.paper import Paper, JournalPaper, ConferencePaper, journal_association_table, conference_association_table
from database.affiliation import Affiliation

engine = create_engine("sqlite:///:memory:", echo=False)
# engine = create_engine("sqlite:///db.sqlite3", echo=False)


def start_database():
    Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    SessionObject = Session()
    return SessionObject


def database_schema_png():
    """Creates and .png with a schema of the database"""
    # remember to change the engine to one which is persistent
    Session = start_database()
    graph = create_schema_graph(metadata=MetaData("sqlite:///db.sqlite3"),
                                show_datatypes=False,  # The image would get nasty big if we"d show the datatypes
                                show_indexes=False,  # ditto for indexes
                                rankdir="LR",  # From left to right (instead of top to bottom)
                                concentrate=False  # Don"t try to join the relation lines together
                                )
    graph.write_png("dbschema.png")  # write out the file
