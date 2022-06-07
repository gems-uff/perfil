import os
from flask import Flask, render_template, jsonify, send_from_directory
import populate_database
from config import collaboration_graphs_alpha, collaboration_graphs_alpha_decay
from collaboration_graphs.generate_graphs import generate_graphs


template_dir = os.getcwd() + os.sep + "collaboration_graphs" + os.sep + "templates"
application = Flask("Collaboration Graphs", template_folder=template_dir)
graphs = None


@application.before_first_request
def populate_graphs():
    global graphs
    session = populate_database.main()
    graphs = generate_graphs(session).copy()


@application.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")


@application.route("/get-data", methods=["GET"])
def get_graphs():
    return jsonify(graphs)


@application.route("/get-alpha-and-decay", methods=["GET"])
def get_alpha():
    return jsonify(collaboration_graphs_alpha, collaboration_graphs_alpha_decay)


if __name__ == "__main__":
    application.run(debug=True)