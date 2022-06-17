from database.entities.researcher import Researcher
from config import start_year, end_year


def link_in_links(link_list, researcher_name, coauthor):
    """Checks if an link already exists in a digraph. If it does, adds 1 to its weight"""

    for dict in link_list:
        if (dict["source"] == researcher_name) and (dict["target"] == coauthor):
            dict["weight"] += 1
            return True
    return False


def add_link(coauthor, links, researcher_name, researchers_in_db):
    if (coauthor != researcher_name) and (coauthor in researchers_in_db) and not link_in_links(links, researcher_name, coauthor):  # creates the link
        link = dict()
        link["source"] = researcher_name
        link["target"] = coauthor
        link["weight"] = 1
        links.append(link)


def populate_links(graphs, researcher_name, paper_list, researchers_in_db):
    """Populates the links of all collaboration digraphs"""

    for paper in paper_list:
        if str(paper.year) in graphs:
            links_year = graphs[str(paper.year)]["links"]
            links_all = graphs["Tudo"]["links"]

            for coauthor in paper.authors.split(";"):
                add_link(coauthor, links_year, researcher_name, researchers_in_db)
                add_link(coauthor, links_all, researcher_name, researchers_in_db)


def digraph_to_graph(graphs):
    """Removes the link with less weight transforming the a digraph to a graph"""

    new_graphs = graphs.copy()

    for year in new_graphs:
        links_list = new_graphs[year]["links"]
        new_link_list = links_list.copy()

        for i in range(len(links_list)):
            link = links_list[i]
            for j in range(i + 1, len(links_list)):
                other_link = links_list[j]

                if (other_link["source"] == link["target"]) and (other_link["target"] == link["source"]):

                    if (other_link in new_link_list) and (link["weight"] >= other_link["weight"]): new_link_list.remove(other_link)
                    elif (link in new_link_list) and (link["weight"] < other_link["weight"]): new_link_list.remove(link)

        new_graphs[year]["links"] = new_link_list

    return new_graphs


def generate_graphs(session):
    """Creates the collaboration digraphs for each year, then transforms them in graphs"""

    graphs = dict()
    for year in range(start_year, end_year + 1):
        graphs[str(year)] = {
            "nodes": [],
            "links": []
        }

    graphs["Tudo"] = {
        "nodes": [],
        "links": []
    }

    researchers_in_db = session.query(Researcher).all()
    researchers_names = [researcher.name for researcher in researchers_in_db]

    for researcher in researchers_in_db:
        node = dict()  # populate nodes
        node["id"] = researcher.name
        for year in graphs:
            graphs[year]["nodes"].append(node)

        populate_links(graphs, researcher.name, researcher.journal_papers, researchers_names)
        populate_links(graphs, researcher.name, researcher.conference_papers, researchers_names)

    graphs = digraph_to_graph(graphs)

    return graphs
