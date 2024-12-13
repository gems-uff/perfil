from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    manager = Column(String)
    team = Column(String)
    start_year = Column(Integer)
    end_year = Column(Integer)
    memberships = relationship('Membership', back_populates='project')


    def __repr__(self):
        return str(self.__dict__)


class Membership(Base):
    __tablename__ = "researcher_project"

    project_id = Column(Integer, ForeignKey('project.id'), primary_key=True)
    researcher_id = Column(Integer, ForeignKey('researcher.id'), primary_key=True)
    principal_investigator = Column(Boolean)
    project = relationship('Project', back_populates='memberships')
    researcher = relationship('Researcher', back_populates='memberships')

    def __repr__(self):
        return str(self.__dict__)