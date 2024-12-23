import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from database.base import Base
from sqlalchemy.orm import relationship


class Researcher(Base):
    __tablename__ = "researcher"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_lattes_update = Column(String)
    phd_college = Column(String)
    phd_defense_year = Column(Integer, default=0)
    google_scholar_id = Column(String)
    lattes_id = Column(Integer)
    memberships = relationship('Membership', back_populates='researcher')
    advisements = relationship('Advisement', back_populates='researcher')
    prizes = relationship('Prize', back_populates='researcher')
    educations = relationship('Education', back_populates='researcher')


    def __repr__(self):
        return str(self.__dict__)


class Affiliation(Base):
    __tablename__ = "affiliation"

    name = Column(String)
    researcher = Column(Integer, ForeignKey("researcher.id"), primary_key=True)
    year = Column(Integer, primary_key=True)

    def __repr__(self):
        return str(self.__dict__)
    

class EducationType(enum.Enum):
    DOCTORATE = 'doutorado'
    POSTDOC = 'posdoc'


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True)
    researcher_id = Column(Integer, ForeignKey("researcher.id"))
    researcher = relationship("Researcher", back_populates="educations")
    type = Column(String)
    course = Column(String)
    area = Column(String)
    institution = Column(String)
    start_date = Column(Integer)
    end_date = Column(Integer)
    status = Column(String)

    def __repr__(self):
        return str(self.__dict__)