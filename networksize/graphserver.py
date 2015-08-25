from crawler import *
from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route("/")
def index():
    info = {"nodes":app.network.GetNodes(), "edges":app.network.GetEdges()}
    return jsonify({"result": info})


@app.route("/randomNode")
def random_node():
    node = app.crawler.get_random_node()
    return jsonify({"result": node})


@app.route("/highestDegreeNode")
def highest_degree_node():
    node = app.crawler.get_highest_degree_node()
    return jsonify({"result": node})


@app.route("/connectedNodes/<node>")
def connected_nodes(node):
    nodes = app.crawler.get_connected_nodes(int(node))
    return jsonify({"result": nodes})


@app.route("/degreeOfNode/<node>")
def degree_of_node(node):
    degree = app.crawler.get_degree_of_node(int(node))
    return jsonify({"result": degree})


@app.route("/connectedNodesWithDegrees/<node>")
def connected_nodes_with_degrees(node):
    connected_nodes = app.crawler.get_connected_nodes_with_degrees(int(node))
    return jsonify({"result": connected_nodes})


class GraphServer:
    def __init__(self, graph, debug=False):
        # global
        app.debug = debug
        app.network = graph
        app.crawler = SnapGraphCrawler(graph)

    def run(self, port=5005):
        app.run(port=port)
