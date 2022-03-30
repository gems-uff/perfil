import uuid
from enum import Enum
from sqlalchemy import or_, not_, and_
from database.entities.titles_support import ResearcherAdvisement, AdvisementsTypes, CommitteeTypes, ResearcherCommittee
from utils.log import log_primary_key_error


class AdvisorOrCommittee(Enum):
    # Enum to help the add_students function
    ADVISOR = "DE-ORIENTACOES-CONCLUIDAS-PARA"
    ADVISOR_OTHERS = "DE-OUTRAS-ORIENTACOES-CONCLUIDAS"
    COMMITTEE = "DA-PARTICIPACAO-EM-BANCA-DE"
    CIVIL_SERVICE_COMMITTEE = "DA-BANCA-JULGADORA-PARA-CONCURSO-PUBLICO"


class Degree(Enum):
    # Enum to help the add_students function
    NOT_DEFINED = ""
    BACHELOR = "GRADUACAO"
    SPECIALIZATION = "APERFEICOAMENTO-ESPECIALIZACAO"
    QUALIFICATION = "EXAME-QUALIFICACAO"
    MASTER = "MESTRADO"
    PHD = "DOUTORADO"


def add_researcher_advisements(session, tree, researcher_id):
    """Call functions to populate the ResearcherAdvisement table"""
    students_advised = tree.xpath("/CURRICULO-VITAE/OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS")[0]

    students_advised_masters = students_advised.findall("ORIENTACOES-CONCLUIDAS-PARA-MESTRADO")
    students_advised_phds = students_advised.findall("ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO")
    students_advised_others = students_advised.findall("OUTRAS-ORIENTACOES-CONCLUIDAS")

    add_titles_support_from_element_list(session, students_advised_masters, AdvisorOrCommittee.ADVISOR, Degree.MASTER,
                                         researcher_id)
    add_titles_support_from_element_list(session, students_advised_phds, AdvisorOrCommittee.ADVISOR, Degree.PHD,
                                         researcher_id)
    add_titles_support_from_element_list(session, students_advised_others, AdvisorOrCommittee.ADVISOR_OTHERS,
                                         Degree.NOT_DEFINED, researcher_id)


def add_researcher_committees(session, tree, researcher_id):
    """Call functions to populate the ReseacherCommittee table"""
    students_judged = tree.xpath("/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO")[0]
    students_judged_bachelor = students_judged.findall("PARTICIPACAO-EM-BANCA-DE-GRADUACAO")
    students_judged_specialization = students_judged.findall("PARTICIPACAO-EM-BANCA-DE-APERFEICOAMENTO-ESPECIALIZACAO")
    students_judged_qualification = students_judged.findall("PARTICIPACAO-EM-BANCA-DE-EXAME-QUALIFICACAO")
    students_judged_masters = students_judged.findall("PARTICIPACAO-EM-BANCA-DE-MESTRADO")
    students_judged_phds = students_judged.findall("PARTICIPACAO-EM-BANCA-DE-DOUTORADO")

    add_titles_support_from_element_list(session, students_judged_bachelor, AdvisorOrCommittee.COMMITTEE,
                                         Degree.BACHELOR, researcher_id)
    add_titles_support_from_element_list(session, students_judged_specialization, AdvisorOrCommittee.COMMITTEE,
                                         Degree.SPECIALIZATION, researcher_id)
    add_titles_support_from_element_list(session, students_judged_qualification, AdvisorOrCommittee.COMMITTEE,
                                         Degree.QUALIFICATION, researcher_id)
    add_titles_support_from_element_list(session, students_judged_masters, AdvisorOrCommittee.COMMITTEE, Degree.MASTER,
                                         researcher_id)
    add_titles_support_from_element_list(session, students_judged_phds, AdvisorOrCommittee.COMMITTEE, Degree.PHD,
                                         researcher_id)

    civil_servants_judged = tree.xpath("/CURRICULO-VITAE/DADOS-COMPLEMENTARES/PARTICIPACAO-EM-BANCA-JULGADORA/BANCA"
                                       "-JULGADORA-PARA-CONCURSO-PUBLICO")

    add_titles_support_from_element_list(session, civil_servants_judged, AdvisorOrCommittee.CIVIL_SERVICE_COMMITTEE,
                                         Degree.NOT_DEFINED, researcher_id)


def add_titles_support_from_element_list(session, element_list, advisor_or_committee: AdvisorOrCommittee,
                                         degree: Degree,
                                         researcher_id):
    """Populates the ReseacherAdviser or ResearcherCommittee tables according with the parameters recivied"""
    advisor_or_committee = advisor_or_committee.value
    degree = degree.value
    details_string = "DETALHAMENTO-" + advisor_or_committee.upper()
    basic_data_string = "DADOS-BASICOS-" + advisor_or_committee.upper()
    if degree != "":
        details_string += "-" + degree.upper()
        basic_data_string += "-" + degree.upper()

    for element in element_list:
        details = element.findall(details_string)[0]

        name = str(uuid.uuid4())
        if AdvisorOrCommittee.CIVIL_SERVICE_COMMITTEE.value not in advisor_or_committee:
            name = details.get("NOME-DO-CANDIDATO") if advisor_or_committee in AdvisorOrCommittee.COMMITTEE.value \
                else details.get("NOME-DO-ORIENTADO")

        college = details.get("NOME-DA-INSTITUICAO") if ((advisor_or_committee in AdvisorOrCommittee.ADVISOR.value) or
                                                         (advisor_or_committee in AdvisorOrCommittee.ADVISOR_OTHERS.value)) else details.get(
            "NOME-INSTITUICAO")

        basic_data = element.findall(basic_data_string)[0]

        title = basic_data.get("TITULO")
        year = basic_data.get("ANO")
        nature = basic_data.get("NATUREZA")

        if (AdvisorOrCommittee.COMMITTEE.value in advisor_or_committee) or \
                (AdvisorOrCommittee.CIVIL_SERVICE_COMMITTEE.value in advisor_or_committee):

            add_researcher_committee_in_bd(college, degree, element, name, nature, researcher_id, session, title, year)

        else:
            add_researcher_advisement_in_bd(college, degree, name, nature, researcher_id, session, title, year)


def add_researcher_committee_in_bd(college, degree, element, name, nature, researcher_id, session, title, year):
    team = ""
    for member in element.findall("PARTICIPANTE-BANCA"):
        team += member.get("NOME-COMPLETO-DO-PARTICIPANTE-DA-BANCA") + ";"
    team = team[:-1]
    type = committee_type_switch(degree, nature)
    lattes_duplication = session.query(ResearcherCommittee).filter(
        and_(researcher_id == ResearcherCommittee.researcher_id, name == ResearcherCommittee.student_name,
             type == ResearcherCommittee.type)).all()
    if len(lattes_duplication) > 0:
        log_primary_key_error("reseacher_committee", researcher_id, name, type)
    else:
        session.add(ResearcherCommittee(researcher_id=researcher_id, student_name=name, college=college,
                                        year=year, title=title, type=type, team=team))


def add_researcher_advisement_in_bd(college, degree, name, nature, researcher_id, session, title, year):
    type = advisor_type_switch(degree, nature)
    lattes_duplication = session.query(ResearcherAdvisement).filter(
        and_(ResearcherAdvisement.researcher_id == researcher_id, ResearcherAdvisement.student_name == name,
             ResearcherAdvisement.type == type, ResearcherAdvisement.year == year)).all()
    if type is not None and len(lattes_duplication) == 0:
        session.add(ResearcherAdvisement(researcher_id=researcher_id, student_name=name, college=college,
                                         year=year, title=title, type=type))
    elif len(lattes_duplication) > 0:
        print(lattes_duplication)
        log_primary_key_error("researcher_advisement", researcher_id, name, type, year)


def advisor_type_switch(degree, nature):
    """Auxiliar funtion to decide the type of the advisement"""
    type_others = {
        "TRABALHO_DE_CONCLUSAO_DE_CURSO_GRADUACAO": AdvisementsTypes.BACHELOR,
        "MONOGRAFIA_DE_CONCLUSAO_DE_CURSO_APERFEICOAMENTO_E_ESPECIALIZACAO": AdvisementsTypes.SPECIALIZATION,
        "INICIACAO_CIENTIFICA": AdvisementsTypes.UNDERGRATUATE_RESEARCH
    }

    if "" == degree and nature in type_others: return type_others[nature]

    type = {
        Degree.MASTER.value: AdvisementsTypes.MASTER,
        Degree.PHD.value: AdvisementsTypes.PHD
    }

    if degree in type: return type[degree]
    return None


def committee_type_switch(degree, nature):
    """Auxiliar funtion to decide the type of the committee"""
    if "Concurso" in nature: return CommitteeTypes.CIVIL_SERVICE_EXAMINATION

    type = {
        Degree.BACHELOR.value: CommitteeTypes.BACHELOR,
        Degree.SPECIALIZATION.value: CommitteeTypes.SPECIALIZATION,
        Degree.MASTER.value: CommitteeTypes.MASTER,
        Degree.PHD.value: CommitteeTypes.PHD,
        Degree.NOT_DEFINED: CommitteeTypes.CIVIL_SERVICE_EXAMINATION
    }

    if Degree.QUALIFICATION.value not in degree: return type[degree]

    type_qualification = {
        "Exame de qualificao de mestrado": CommitteeTypes.MASTER_QUALIFICATION,
        "Exame de qualificao de doutorado": CommitteeTypes.PHD_QUALIFICATION
    }

    return type_qualification[nature[:18] + nature[nature.index("o de"):len(
        nature)]]  # can change the switch to only 'mestrado' or 'doutorado'
