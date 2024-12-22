import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from database.base import Base
from sqlalchemy.orm import relationship


class AdvisementsTypes(enum.Enum):
    BACHELOR = "graduação"
    MASTER = "mestrado"
    PHD = "doutorado"
    SPECIALIZATION = "especialização"
    UNDERGRADUATE_RESEARCH = "iniciação científica"


class CommitteeTypes(enum.Enum):
    BACHELOR = "graduação"
    MASTER = "mestrado"
    MASTER_QUALIFICATION = "qualificação de mestrado"
    PHD = "doutorado"
    PHD_QUALIFICATION = "qualificação de doutorado"
    SPECIALIZATION = "especialização"
    CIVIL_SERVICE_EXAMINATION = "concurso público"


class Advisement(Base):
    __tablename__ = "researcher_advisement"

    id = Column(Integer, primary_key=True)
    researcher_id = Column(Integer, ForeignKey("researcher.id"))
    researcher = relationship("Researcher", back_populates="advisements")
    student_name = Column(String)
    college = Column(String)
    year = Column(Integer)
    title = Column(String)
    type = Column(Enum(AdvisementsTypes))
    # committee = Column(String)

    def __repr__(self):
        return str(self.__dict__)


class Committee(Base):
    __tablename__ = "researcher_committee"

    id = Column(Integer, primary_key=True)
    researcher_id = Column(Integer, ForeignKey("researcher.id"))
    student_name = Column(String)
    college = Column(String)
    year = Column(Integer)
    title = Column(String)  # if it's a civil service entrance examination, use the name of the job as title
    type = Column(Enum(CommitteeTypes))
    team = Column(String)

    def __repr__(self):
        return str(self.__dict__)
