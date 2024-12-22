from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy_schemadisplay import create_schema_graph

from database.base import Base
from database.entities.venue import Venue, Conference, Journal
from database.entities.titles_support import Advisement, Committee
from database.entities.project import Project, Membership
from database.entities.researcher import Researcher, Affiliation
from database.entities.paper import Paper, JournalPaper, ConferencePaper, journal_association_table, conference_association_table
from database.entities.book import BookManuscript, Book, BookChapter, ResearcherPublishedBook, ResearcherPublishedBookChapter
from database.entities.other_works import Patent, EditorialBoard, ConferenceOrganization, ResearcherPatent

from config import output_path

def start_database(sqlite: bool):
    """Starts the database returning the session"""
    engine = create_engine("sqlite:///:memory:", echo=False)
    if sqlite:
        print(f'sqlite:///{output_path}mysql.db')
        engine = create_engine(f'sqlite:///{output_path}mysql.db', echo=False)

    Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    SessionObject = Session()
    return SessionObject


def database_schema_png():
    """Creates and .png with a schema of the database"""
    # remember to change the engine to one which is persistent
    start_database(True)
    graph = create_schema_graph(metadata=MetaData("sqlite:///db.sqlite3"),
                                show_datatypes=False,  # The image would get nasty big if we"d show the datatypes
                                show_indexes=False,  # ditto for indexes
                                rankdir="LR",  # From left to right (instead of top to bottom)
                                concentrate=False  # Don"t try to join the relation lines together
                                )
    graph.write_png("dbschema.png")  # write out the file
