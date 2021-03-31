import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database.base import Base
from database.researcher import Researcher


class Type(enum.Enum):
    master_advisor = "master_advisor"
    phd_advisor = "phd_advisor"
    master_comittee = "master_comittee"
    phd_comittee = "phd_comittee"


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return str(self.__dict__)


class ResearcherStudent(Base):
    __tablename__ = "researcher_student"

    researcher_id = Column(Integer, ForeignKey("researcher.id"), primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)
    type = Column(Enum(Type), primary_key=True)
    year = Column(Integer)
    title = Column(String)
    committee = Column(String)

    researchers = relationship("Researcher", backref="students")
    students = relationship("Student", backref="researchers")

    def __repr__(self):
        return str(self.__dict__)