from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base


class BookManuscript(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    publisher = Column(String)
    year = Column(Integer)
    authors = Column(String)
    doi = Column(String)

    type = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "book",
        "polymorphic_on": type
    }

    def __repr__(self):
        return str(self.__dict__)


class Book(BookManuscript):
    __tablename__ = "published_book"

    id = Column(Integer, ForeignKey("book.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "published_book"
    }

    def __repr__(self):
        return str(self.__dict__)


class BookChapter(BookManuscript):
    __tablename__ = "published_book_chapter"

    id = Column(Integer, ForeignKey("book.id"), primary_key=True)
    chapter_title = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "published_book_chapter"
    }


class ResearcherPublishedBook(Base):
    __tablename__ = "researcher_published_book"

    published_book_id = Column(Integer, ForeignKey('published_book.id'), primary_key=True)
    researcher_id = Column(Integer, ForeignKey('researcher.id'), primary_key=True)

    def __repr__(self):
        return str(self.__dict__)


class ResearcherPublishedBookChapter(Base):
    __tablename__ = "researcher_published_book_chapter"

    published_book_chapter_id = Column(Integer, ForeignKey('published_book_chapter.id'), primary_key=True)
    researcher_id = Column(Integer, ForeignKey('researcher.id'), primary_key=True)

    def __repr__(self):
        return str(self.__dict__)