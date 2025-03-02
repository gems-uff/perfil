from sqlalchemy import or_, and_, func
from database.entities.researcher import Researcher
from database.entities.book import Book, ResearcherPublishedBook, BookChapter, ResearcherPublishedBookChapter
from utils.log import log_possible_lattes_duplication, log_unify
from config import unify_book, unify_chapter


def get_or_add_book_id(session, basic_data, details, book_authors, researcher_id, researcher_name):
    '''Gets the published book already on the database or adds it'''
    title = basic_data.get("TITULO-DO-LIVRO")
    year = basic_data.get("ANO")
    doi = basic_data.get("DOI")

    book_list = session.query(Book).filter(
        and_(func.lower(Book.title) == func.lower(title), Book.year == year)).all() if doi is None or doi == "" else \
        session.query(Book).filter(Book.doi == doi).all()

    # Normalize
    if unify_book and (len(book_list) > 0):
        log_unify(book_list[0].title, researcher_id, researcher_name)
        return book_list[0]

    publisher = details.get("NOME-DA-EDITORA")
    authors = ""

    for author in book_authors:
        authors += author.get("NOME-COMPLETO-DO-AUTOR") + ";"
    authors = authors[:-1]

    new_book = Book(title=title, publisher=publisher, year=year, authors=authors, doi=doi)
    session.add(new_book)

    return new_book


def add_researcher_published_books(session, tree, researcher):
    '''Adds all the published books from a lattes .xml file'''
    books = tree.xpath(
        "/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/LIVROS-E-CAPITULOS/LIVROS-PUBLICADOS-OU-ORGANIZADOS/LIVRO-PUBLICADO-OU-ORGANIZADO")
    researcher_name = researcher.name

    for book in books:
        basic_data = book.findall("DADOS-BASICOS-DO-LIVRO")[0]
        details = book.findall("DETALHAMENTO-DO-LIVRO")[0]
        book_authors = book.findall("AUTORES")
        added_book = get_or_add_book_id(session, basic_data, details, book_authors, researcher.id, researcher_name)

        # Lattes duplication
        this_researcher_books_relationship = session.query(ResearcherPublishedBook.published_book_id).filter(ResearcherPublishedBook.researcher_id == researcher.id)
        this_researcher_books_in_db = session.query(Book).filter(
            or_(and_(Book.doi == added_book.doi, added_book.doi is not None, Book.doi != ""), and_(Book.year == added_book.year, func.lower(Book.title) == func.lower(added_book.title))),
            Book.id.in_(this_researcher_books_relationship)).all()
        for book_in_bd in this_researcher_books_in_db:
            log_possible_lattes_duplication("researcher_published_book", researcher_name, researcher.id,
                                            book_in_bd.id, book_in_bd.title, book_in_bd.year, book_in_bd.doi)

        # If not unified, it will always be True, because the added_book is going to be a new one
        relationship_not_in_db = len(session.query(ResearcherPublishedBook).filter(ResearcherPublishedBook.researcher_id == researcher.id,
                                                                                   ResearcherPublishedBook.published_book_id == added_book.id).all()) == 0

        if relationship_not_in_db:
            session.add(ResearcherPublishedBook(published_book_id=added_book.id, researcher_id=researcher.id))


def get_or_add_chapter_id(session, basic_data, details, chapter_authors, researcher_id, researcher_name):
    '''Gets a chapter from a published book already on the database or adds the chapter'''
    chapter_title = basic_data.get("TITULO-DO-CAPITULO-DO-LIVRO")
    year = basic_data.get("ANO")
    doi = basic_data.get("DOI")

    chapter_list = session.query(BookChapter).filter(func.lower(BookChapter.chapter_title) == func.lower(chapter_title),
                                                     BookChapter.year == year).all() if doi is None \
        else session.query(BookChapter).filter(func.lower(BookChapter.doi == doi)).all()

    # Normalize
    if unify_chapter and (len(chapter_list) > 0):  # Normalize
        log_unify(chapter_list[0].title, researcher_id, researcher_name)
        return chapter_list[0]

    publisher = details.get("NOME-DA-EDITORA")
    book_title = details.get("TITULO-DO-LIVRO")
    authors = ""

    for author in chapter_authors:
        authors += author.get("NOME-COMPLETO-DO-AUTOR") + ";"
    authors = authors[:-1]

    new_chapter = BookChapter(title=book_title, publisher=publisher, year=year, authors=authors,
                              chapter_title=chapter_title)
    session.add(new_chapter)

    return new_chapter


def add_researcher_published_chapters(session, tree, researcher):
    '''Adds all the chapters of published books from a lattes .xml file'''
    chapters_of_books = tree.xpath(
        "/CURRICULO-VITAE/PRODUCAO-BIBLIOGRAFICA/LIVROS-E-CAPITULOS/CAPITULOS-DE-LIVROS-PUBLICADOS/CAPITULO-DE-LIVRO-PUBLICADO")
    researcher_name = researcher.name

    for chapter in chapters_of_books:
        basic_data = chapter.findall("DADOS-BASICOS-DO-CAPITULO")[0]
        details = chapter.findall("DETALHAMENTO-DO-CAPITULO")[0]
        chapter_authors = chapter.findall("AUTORES")
        added_chapter = get_or_add_chapter_id(session, basic_data, details, chapter_authors, researcher.id, researcher_name)

        # Lattes duplication
        this_researcher_chapters_relationship = session.query(ResearcherPublishedBookChapter.published_book_chapter_id).filter(ResearcherPublishedBookChapter.researcher_id == researcher.id)
        this_researcher_chapters_in_db = session.query(BookChapter).filter(
            or_(and_(BookChapter.doi == added_chapter.doi, added_chapter.doi is not None, BookChapter.doi != ""), and_(BookChapter.year == added_chapter.year, func.lower(BookChapter.chapter_title) == func.lower(added_chapter.chapter_title))),
            BookChapter.id.in_(this_researcher_chapters_relationship)).all()
        for chapter_in_bd in this_researcher_chapters_in_db:
            log_possible_lattes_duplication("researcher_published_book", researcher_name, researcher.id,
                                            chapter_in_bd.id, chapter_in_bd.chapter_title, chapter_in_bd.year, chapter_in_bd.doi)

        # If not unified, it will always be True, because the added_chapter is going to be a new one
        relationship_not_in_db = len(session.query(ResearcherPublishedBookChapter).filter(ResearcherPublishedBookChapter.researcher_id == researcher.id, ResearcherPublishedBookChapter.published_book_chapter_id == added_chapter.id).all()) == 0

        if relationship_not_in_db:
            session.add(ResearcherPublishedBookChapter(published_book_chapter_id=added_chapter.id, researcher_id=researcher.id))