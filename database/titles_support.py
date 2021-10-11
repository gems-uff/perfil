import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from database.base import Base


class AdvisementsTypes(enum.Enum):
    BACHELOR = "bachelor"
    MASTER = "master"
    PHD = "phd"
    SPECIALIZATION = "specialization"
    UNDERGRATUATE_RESEARCH = "undergratuate_research"


class CommitteeTypes(enum.Enum):
    BACHELOR = "bachelor"
    MASTER = "master"
    MASTER_QUALIFICATION = "master_qualification"
    PHD = "phd"
    PHD_QUALIFICATION = "phd_qualification"
    SPECIALIZATION = "specialization"
    CIVIL_SERVICE_EXAMINATION = "civil_service_examination"


class ResearcherAdvisement(Base):
    __tablename__ = "researcher_advisement"

    researcher_id = Column(Integer, ForeignKey("researcher.id"), primary_key=True)
    student_name = Column(String, primary_key=True)
    college = Column(String)
    year = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(Enum(AdvisementsTypes), primary_key=True)
    # committee = Column(String)

    def __repr__(self):
        return str(self.__dict__)


class ResearcherCommittee(Base):
    __tablename__ = "researcher_committee"

    researcher_id = Column(Integer, ForeignKey("researcher.id"), primary_key=True)
    student_name = Column(String, primary_key=True)
    college = Column(String)
    year = Column(Integer)
    title = Column(String)  # if it's a civil service entrance examination, use the name of the job as title
    type = Column(Enum(CommitteeTypes), primary_key=True)
    team = Column(String)

    def __repr__(self):
        return str(self.__dict__)
