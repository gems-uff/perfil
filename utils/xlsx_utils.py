def calculate_number_of_pages(paper):
    """Calculates the number of pages of a given paper"""
    if (paper.last_page is None) or (paper.first_page is None) \
            or (type(paper.last_page) is not int) or (type(paper.first_page) is not int): return ""
    return paper.last_page - paper.first_page + 1