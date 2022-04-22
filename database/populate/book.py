from sqlalchemy import or_, and_, func
from database.entities.researcher import Researcher
from database.entities.book import PublishedBook, ResearcherPublishedBook, PublishedBookChapter, ResearcherPublishedBookChapter
from utils.log import log_possible_lattes_duplication, log_normalize
from config import normalize_book, normalize_chapter


def get_or_add_book_id(session, basic_data, details, book_authors, researcher_id, researcher_name):
    '''Gets the published book already on the database or adds it'''
    title = basic_data.get("TITULO-DO-LIVRO")
    year = basic_data.get("ANO")
    doi = basic_data.get("DOI")

    book_list = session.query(PublishedBook).filter(
        and_(func.lower(PublishedBook.title) == func.lower(title), PublishedBook.year == year)).all() if doi is None or doi == "" else \
        session.query(PublishedBook).filter(PublishedBook.doi == doi).all()

    # Normalize
    if normalize_book and (len(book_list) > 0):
        log_normalize(book_list[0].title, researcher_id, researcher_name)
        return book_list[0]

    publisher = details.get("NOME-DA-EDITORA")
    authors = ""

    for author in book_authors:
        authors += author.get("NOME-COMPLETO-DO-AUTOR") + ";"
    authors = authors[:-1]

    new_book = PublishedBook(title=title, publisher=publisher, year=year, authors=authors, doi=doi)
    session.add(new_book)
    session.flush()

    return new_book


def add_researcher_published_books(session, tree, researcher_id):
    '''Adds all the published books from a lattes .xml file'''
    books = tree.xpath(
        "/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/LIVROS-E-CAPITULOS/LIVROS-PUBLICADOS-OU-ORGANIZADOS/LIVRO-PUBLICADO-OU-ORGANIZADO")
    researcher_name = session.query(Researcher.name).filter(Researcher.id == researcher_id).all()[0][0]

    for book in books:
        basic_data = book.findall("DADOS-BASICOS-DO-LIVRO")[0]
        details = book.findall("DETALHAMENTO-DO-LIVRO")[0]
        book_authors = book.findall("AUTORES")
        added_book = get_or_add_book_id(session, basic_data, details, book_authors, researcher_id, researcher_name)

        # Lattes duplication
        this_researcher_books_relationship = session.query(ResearcherPublishedBook.published_book_id).filter(ResearcherPublishedBook.researcher_id == researcher_id)
        this_researcher_books_in_db = session.query(PublishedBook).filter(
            or_(and_(PublishedBook.doi == added_book.doi, added_book.doi is not None, PublishedBook.doi != ""), and_(PublishedBook.year == added_book.year, func.lower(PublishedBook.title)==func.lower(added_book.title))),
            PublishedBook.id.in_(this_researcher_books_relationship)).all()
        for book_in_bd in this_researcher_books_in_db:
            log_possible_lattes_duplication("researcher_published_book", researcher_name, researcher_id,
                                            book_in_bd.id, book_in_bd.title, book_in_bd.year, book_in_bd.doi)

        # If not normalize, it will always be True, because the added_book is going to be a new one
        relationship_not_in_db = len(session.query(ResearcherPublishedBook).filter(ResearcherPublishedBook.researcher_id == researcher_id,
                                                                                   ResearcherPublishedBook.published_book_id == added_book.id).all()) == 0

        if relationship_not_in_db:
            session.add(ResearcherPublishedBook(published_book_id=added_book.id, researcher_id=researcher_id))
            session.flush()


def get_or_add_chapter_id(session, basic_data, details, chapter_authors, researcher_id, researcher_name):
    '''Gets a chapter from a published book already on the database or adds the chapter'''
    chapter_title = basic_data.get("TITULO-DO-CAPITULO-DO-LIVRO")
    year = basic_data.get("ANO")
    doi = basic_data.get("DOI")

    chapter_list = session.query(PublishedBookChapter).filter(func.lower(PublishedBookChapter.chapter_title) == func.lower(chapter_title),
                                                              PublishedBookChapter.year == year).all() if doi is None \
        else session.query(PublishedBookChapter).filter(func.lower(PublishedBookChapter.doi == doi)).all()

    # Normalize
    if normalize_chapter and (len(chapter_list) > 0):  # Normalize
        log_normalize(chapter_list[0].title, researcher_id, researcher_name)
        return chapter_list[0]

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

    return new_chapter


def add_researcher_published_chapters(session, tree, researcher_id):
    '''Adds all the chapters of published books from a lattes .xml file'''
    chapters_of_books = tree.xpath(
        "/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/LIVROS-E-CAPITULOS/CAPITULOS-DE-LIVROS-PUBLICADOS/CAPITULO-DE-LIVRO-PUBLICADO")
    researcher_name = session.query(Researcher.name).filter(Researcher.id == researcher_id).all()[0][0]

    for chapter in chapters_of_books:
        basic_data = chapter.findall("DADOS-BASICOS-DO-CAPITULO")[0]
        details = chapter.findall("DETALHAMENTO-DO-CAPITULO")[0]
        chapter_authors = chapter.findall("AUTORES")
        added_chapter = get_or_add_chapter_id(session, basic_data, details, chapter_authors, researcher_id, researcher_name)

        # Lattes duplication
        this_researcher_chapters_relationship = session.query(ResearcherPublishedBookChapter.published_book_chapter_id).filter(ResearcherPublishedBookChapter.researcher_id == researcher_id)
        this_researcher_chapters_in_db = session.query(PublishedBookChapter).filter(
            or_(and_(PublishedBookChapter.doi == added_chapter.doi, added_chapter.doi is not None, PublishedBookChapter.doi != ""), and_(PublishedBookChapter.year == added_chapter.year, func.lower(PublishedBookChapter.title) == func.lower(added_chapter.title))),
            PublishedBookChapter.id.in_(this_researcher_chapters_relationship)).all()
        for chapter_in_bd in this_researcher_chapters_in_db:
            log_possible_lattes_duplication("researcher_published_book", researcher_name, researcher_id,
                                            chapter_in_bd.id, chapter_in_bd.chapter_title, chapter_in_bd.year, chapter_in_bd.doi)

        # If not normalize, it will always be True, because the added_chapter is going to be a new one
        relationship_not_in_db = len(session.query(ResearcherPublishedBookChapter).filter(ResearcherPublishedBookChapter.researcher_id == researcher_id, ResearcherPublishedBookChapter.published_book_chapter_id == added_chapter.id).all()) == 0

        if relationship_not_in_db:
            session.add(ResearcherPublishedBookChapter(published_book_chapter_id=added_chapter.id, researcher_id=researcher_id))
            session.flush()
