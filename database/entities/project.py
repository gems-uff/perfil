from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from database.entities.researcher import Researcher


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    manager = Column(String)
    team = Column(String)
    start_year = Column(Integer)
    end_year = Column(Integer)

    def __repr__(self):
        return str(self.__dict__)


class Membership(Base):
    __tablename__ = "researcher_project"

    project_id = Column(Integer, ForeignKey('project.id'), primary_key=True)
    researcher_id = Column(Integer, ForeignKey('researcher.id'), primary_key=True)
    principal_investigator = Column(Boolean)

    def __repr__(self):
        return str(self.__dict__)