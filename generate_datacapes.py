import openpyxl
import os
import populate_database
from collections import defaultdict
from config import generate_datacapes_output_dir
from database.database_manager import Researcher, Journal, Conference, ConferencePaper, JournalPaper, Paper
from database.entities.venue import QualisLevel
from utils.xlsx_utils import calculate_number_of_pages
from utils.list_filters import scope_years_paper_or_support, published_journal_paper, jcr_pub_filter, \
    qualis_level_journal, qualis_level_conference, conference_paper, journal_paper


def write_production_paper(paper, researcher, row, venue, worksheet, is_journal_paper : bool, write_researcher : bool):
    column_number_additional = 0
    if(write_researcher):
        worksheet.cell(row=row, column=1, value=researcher.name)
        worksheet.cell(row=row, column=2, value=researcher.last_lattes_update)
        column_number_additional = 2
    worksheet.cell(row=row, column=1+column_number_additional, value=paper.year)
    worksheet.cell(row=row, column=2+column_number_additional, value="PERIODICO" if is_journal_paper else "CONFERENCIA")
    worksheet.cell(row=row, column=3+column_number_additional, value=paper.title)
    worksheet.cell(row=row, column=4+column_number_additional, value=venue.name)
    worksheet.cell(row=row, column=5+column_number_additional, value=calculate_number_of_pages(paper))
    worksheet.cell(row=row, column=6+column_number_additional, value=venue.qualis.value if venue.qualis is not None else "null")
    worksheet.cell(row=row, column=7+column_number_additional, value=venue.jcr if is_journal_paper else "null")
    worksheet.cell(row=row, column=8+column_number_additional, value=venue.forum_oficial)


def reseacher_production_paper_iterator(array_papers, researcher, session, worksheet, row, is_journal_paper : bool):
    for i in range(len(array_papers)):
        paper = array_papers[i]
        venue = session.query(Journal).filter(paper.venue == Journal.id).all()[0] if is_journal_paper \
            else session.query(Conference).filter(paper.venue == Conference.id).all()[0]

        write_production_paper(paper, researcher, row, venue, worksheet, is_journal_paper, True)
        row += 1
    return row


def write_reseachers_production(researchers, session):
    wb = openpyxl.Workbook()
    worksheet = wb.active
    row = 1
    papers = []
    for researcher in researchers:
        conference_papers = list(filter(scope_years_paper_or_support, researcher.conference_papers))
        row = reseacher_production_paper_iterator(conference_papers, researcher, session, worksheet, row, False)

        journal_papers = list(filter(published_journal_paper,list(filter(scope_years_paper_or_support, researcher.journal_papers))))
        row = reseacher_production_paper_iterator(journal_papers, researcher, session, worksheet, row, True)

        papers += conference_papers
        papers += journal_papers

    wb.save(generate_datacapes_output_dir + os.sep + "producao_docentes.xlsx")

    return papers


def write_yearly_production(papers, session):
    papers.sort(key=lambda paper: paper.year)
    wb = openpyxl.Workbook()
    worksheet = wb.active
    for i in range(len(papers)):
        is_journal_paper = isinstance(papers[i], JournalPaper)
        venue = session.query(Journal).filter(papers[i].venue == Journal.id).all()[0] if is_journal_paper \
            else session.query(Conference).filter(papers[i].venue == Conference.id).all()[0]
        write_production_paper(papers[i], None, i + 1, venue, worksheet, is_journal_paper, False)
    wb.save(generate_datacapes_output_dir + os.sep + "producao_anual.xlsx")


def write_summary_header_papers(column, periodico, worksheet):
    for qualis_level in QualisLevel:
        worksheet.cell(row=1, column=column, value=periodico + " " + qualis_level.value)
        column += 1
    return column


def write_summary_header(worksheet):
    worksheet.cell(row=1, column=1, value="ENTIDADE")
    worksheet.cell(row=1, column=2, value="PERIODICOS JCR")
    column = 3
    column = write_summary_header_papers(column, "PERIODICO", worksheet)
    column = write_summary_header_papers(column, "CONFERENCIA", worksheet)
    worksheet.cell(row=1, column=column, value="I-RESTRITO PERIODICO")
    worksheet.cell(row=1, column=column + 1, value="I-RESTRITO CONFERENCIA")
    worksheet.cell(row=1, column=column + 2, value="I-RESTRITO TOTAL")
    worksheet.cell(row=1, column=column + 3, value="I-GERAL PERIODICO")
    worksheet.cell(row=1, column=column + 4, value="I-GERAL CONFERENCIA")
    worksheet.cell(row=1, column=column + 5, value="I-GERAL TOTAL")
    worksheet.cell(row=1, column=column + 6, value="SATURACAO (TRAVA)")
    worksheet.cell(row=1, column=column + 7, value="SIM-CRED-2019")


def qualis_weight(qualis_level: QualisLevel):
    weight = {
        QualisLevel.A1: 1,
        QualisLevel.A2: 0.85,
        QualisLevel.B1: 0.7,
        QualisLevel.B2: 0.5,
        QualisLevel.B3: 0.2,
        QualisLevel.B4: 0.1,
        QualisLevel.B5: 0.05,
        QualisLevel.C: 0,
        QualisLevel.NC: 0
    }

    return weight[qualis_level]


def write_paper_number_by_qualis(session, column, journal_papers, row, worksheet, filter_function):
    restricted_index = 0
    general_index = 0

    for qualis_level in QualisLevel:
        papers = list(filter(lambda x: filter_function(x, session, qualis_level), journal_papers))
        worksheet.cell(row=row, column=column, value=len(papers))

        if qualis_level in [QualisLevel.A1, QualisLevel.A2, QualisLevel.B1]: restricted_index += len(papers) * qualis_weight(qualis_level)
        general_index += len(papers) * qualis_weight(qualis_level)

        column += 1

    return restricted_index, general_index


def write_summary(conference_papers, journal_papers, journal_papers_jcr, entity, row, session, worksheet):
    worksheet.cell(row=row, column=1, value=entity)
    worksheet.cell(row=row, column=2, value=len(journal_papers_jcr))
    journal_indexes = write_paper_number_by_qualis(session, 3, journal_papers, row, worksheet, qualis_level_journal)
    conference_indexes = write_paper_number_by_qualis(session, len(QualisLevel) + 3,
                                                      conference_papers, row, worksheet, qualis_level_conference)
    journal_restricted_index = journal_indexes[0]
    conference_restricted_index = conference_indexes[0]
    journal_general_index = journal_indexes[1]
    conference_general_index = conference_indexes[1]
    column = len(QualisLevel) * 2 + 3
    worksheet.cell(row=row, column=column, value=journal_restricted_index)
    worksheet.cell(row=row, column=column + 1, value=conference_restricted_index)
    worksheet.cell(row=row, column=column + 2, value=journal_restricted_index + conference_restricted_index)
    worksheet.cell(row=row, column=column + 3, value=journal_general_index)
    worksheet.cell(row=row, column=column + 4, value=conference_general_index)
    worksheet.cell(row=row, column=column + 5, value=journal_general_index + conference_general_index)
    if journal_general_index != 0:
        worksheet.cell(row=row, column=column + 6, value=conference_general_index / journal_general_index)
    else:
        if conference_general_index != 0:
            worksheet.cell(row=row, column=column + 6, value="INF.")
        else:
            worksheet.cell(row=row, column=column + 6, value="IND.")
    conference_b2_index = len(
        list(filter(lambda x: qualis_level_conference(x, session, QualisLevel.B2), conference_papers))) \
                          * qualis_weight(QualisLevel.B2)
    worksheet.cell(row=row, column=column + 7,
                   value=journal_restricted_index + conference_restricted_index + conference_b2_index)
    if journal_restricted_index == 0: worksheet.cell(row=row, column=column + 8, value="P=0")


def write_4n_production(papers, session):
    wb = openpyxl.Workbook()
    worksheet = wb.active
    for i in range(len(papers)):
        is_journal_paper = isinstance(papers[i], JournalPaper)
        venue = session.query(Journal).filter(papers[i].venue == Journal.id).all()[0] if is_journal_paper \
            else session.query(Conference).filter(papers[i].venue == Conference.id).all()[0]
        row = i + 1

        worksheet.cell(row=row, column=1, value="PERIODICO" if is_journal_paper else "CONFERENCIA")
        worksheet.cell(row=row, column=2, value=venue.issn if is_journal_paper else venue.acronym)
        worksheet.cell(row=row, column=3, value=papers[i].title)
        worksheet.cell(row=row, column=4, value=papers[i].authors)
        worksheet.cell(row=row, column=5, value=venue.name)
        worksheet.cell(row=row, column=6, value=venue.forum_oficial)
        worksheet.cell(row=row, column=7, value=papers[i].year)
        worksheet.cell(row=row, column=8, value=calculate_number_of_pages(papers[i]))
        worksheet.cell(row=row, column=9, value=venue.qualis.value if venue.qualis is not None else "null")
        worksheet.cell(row=row, column=10, value=venue.jcr if is_journal_paper else "null")

    wb.save(generate_datacapes_output_dir + os.sep + "producao_4n.xlsx")


def write_researchers_summary(researchers, session):
    wb = openpyxl.Workbook()
    worksheet = wb.active
    write_summary_header(worksheet)
    row = 2
    for researcher in researchers:
        conference_papers = list(filter(scope_years_paper_or_support, researcher.conference_papers))
        journal_papers = list(
            filter(published_journal_paper, list(filter(scope_years_paper_or_support, researcher.journal_papers))))
        journal_papers_jcr = list(filter(lambda x: jcr_pub_filter(x, session, 0), journal_papers))

        write_summary(conference_papers, journal_papers, journal_papers_jcr, researcher.name, row, session, worksheet)

        row += 1
    wb.save(generate_datacapes_output_dir + os.sep + "sumario_docentes.xlsx")


def write_yearly_summary(papers, session):
    papers_by_year = defaultdict(list)
    for paper in papers:
        papers_by_year[paper.year].append(paper)
    wb = openpyxl.Workbook()
    worksheet = wb.active
    write_summary_header(worksheet)
    row = 2
    for year in papers_by_year:
        conference_papers = list(filter(conference_paper, papers_by_year[year]))
        journal_papers = list(filter(published_journal_paper, list(filter(journal_paper, papers_by_year[year]))))
        journal_papers_jcr = list(filter(lambda x: jcr_pub_filter(x, session, 0), journal_papers))

        write_summary(conference_papers, journal_papers, journal_papers_jcr, year, row, session, worksheet)

        row += 1
    wb.save(generate_datacapes_output_dir + os.sep + "sumario_anual.xlsx")


def remove_paper_duplicates(papers):
    new_list = papers.copy()
    for i in range(len(papers)):
        for j in range(i + 1, len(papers)):
            if (papers[i].title == papers[j].title):
                new_list.remove(papers[j])
    return new_list


def main():
    session = populate_database.main()
    researchers = session.query(Researcher).all()

    # writes researchers production
    papers = remove_paper_duplicates(write_reseachers_production(researchers, session))
    # writes yearly production
    write_yearly_production(papers, session)
    # writes 4n production
    write_4n_production(papers, session)

    # writes researcher summary
    write_researchers_summary(researchers, session)
    #writes yearly summary
    write_yearly_summary(papers, session)


if __name__ == "__main__":
    main()