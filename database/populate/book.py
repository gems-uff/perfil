from sqlalchemy import and_
from database.entities.researcher import Researcher
from database.entities.book import PublishedBook, ResearcherPublishedBook, PublishedBookChapter, ResearcherPublishedBookChapter
from utils.log import log_primary_key_error


def get_or_add_book_id(session, basic_data, details, book_authors):
    '''Gets the published book already on the database or adds it'''
    title = basic_data.get("TITULO-DO-LIVRO")
    year = basic_data.get("ANO")
    doi = basic_data.get("DOI")

    book_list = session.query(PublishedBook).filter(
        and_(PublishedBook.title == title, PublishedBook.year == year)).all() if doi is None or doi == "" else \
        session.query(PublishedBook).filter(PublishedBook.doi == doi).all()

    if len(book_list) > 0:
        return book_list[0].id

    publisher = details.get("NOME-DA-EDITORA")
    authors = ""

    for author in book_authors:
        authors += author.get("NOME-COMPLETO-DO-AUTOR") + ";"
    authors = authors[:-1]

    new_book = PublishedBook(title=title, publisher=publisher, year=year, authors=authors, doi=doi)
    session.add(new_book)
    session.flush()

    return new_book.id


def add_researcher_published_books(session, tree, researcher_id):
    '''Adds all the published books from a lattes .xml file'''
    books = tree.xpath(
        "/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/LIVROS-E-CAPITULOS/LIVROS-PUBLICADOS-OU-ORGANIZADOS/LIVRO-PUBLICADO-OU-ORGANIZADO")

    for book in books:
        basic_data = book.findall("DADOS-BASICOS-DO-LIVRO")[0]
        details = book.findall("DETALHAMENTO-DO-LIVRO")[0]
        book_authors = book.findall("AUTORES")
        book_id = get_or_add_book_id(session, basic_data, details, book_authors)


        relationship_not_in_db = len(session.query(ResearcherPublishedBook).filter(ResearcherPublishedBook.researcher_id == researcher_id,
                                                                                   ResearcherPublishedBook.published_book_id == book_id).all()) == 0

        if relationship_not_in_db: session.add(ResearcherPublishedBook(published_book_id=book_id, researcher_id=researcher_id))
        else:
            researcher_name = session.query(Researcher.name).filter(Researcher.id == researcher_id).all()[0][0]
            book_name = session.query(PublishedBook.title).filter(PublishedBook.id == book_id).all()[0][0]
            log_primary_key_error("researcher_published_book", researcher_name, researcher_id, book_id, "(" + book_name + ")")



def get_or_add_chapter_id(session, basic_data, details, chapter_authors):
    '''Gets a chapter from a published book already on the database or adds the chapter'''
    chapter_title = basic_data.get("TITULO-DO-CAPITULO-DO-LIVRO")

    chapter_list = session.query(PublishedBookChapter).filter(PublishedBookChapter.chapter_title == chapter_title).all()
    if len(chapter_list) > 0:
        return chapter_list[0].id

    year = basic_data.get("ANO")
    publisher = details.get("NOME-DA-EDITORA")
    book_title = details.get("TITULO-DO-LIVRO")
    authors = ""

    for author in chapter_authors:
        authors += author.get("NOME-COMPLETO-DO-AUTOR") + ";"
    authors = authors[:-1]

    new_chapter = PublishedBookChapter(title=book_title, publisher=publisher, year=year, authors=authors,
                                       chapter_title=chapter_title)
    session.add(new_chapter)
    session.flush()

    return new_chapter.id


def add_researcher_published_chapters(session, tree, researcher_id):
    '''Adds all the chapters of published books from a lattes .xml file'''
    chapters_of_books = tree.xpath(
        "/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/LIVROS-E-CAPITULOS/CAPITULOS-DE-LIVROS-PUBLICADOS/CAPITULO-DE-LIVRO-PUBLICADO")

    for chapter in chapters_of_books:
        basic_data = chapter.findall("DADOS-BASICOS-DO-CAPITULO")[0]
        details = chapter.findall("DETALHAMENTO-DO-CAPITULO")[0]
        chapter_authors = chapter.findall("AUTORES")
        chapter_id = get_or_add_chapter_id(session, basic_data, details, chapter_authors)

        session.add(ResearcherPublishedBookChapter(published_book_chapter_id=chapter_id, researcher_id=researcher_id))