from crawler import *
from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def index():
    info = {"nodes":app.network.GetNodes(), "edges":app.network.GetEdges()}
    return jsonify({"result": info})

@app.route("/randomNode")
def randomNode():
    node = app.crawler.getRandomNode()
    return jsonify({"result": node})

@app.route("/highestDegreeNode")
def highestDegreeNode():
    node = app.crawler.getHighestDegreeNode()
    return jsonify({"result": node})

@app.route("/connectedNodes/<node>")
def connectedNodes(node):
    connectedNodes = app.crawler.getConnectedNodes(int(node))
    return jsonify({"result": connectedNodes})

@app.route("/degreeOfNode/<node>")
def degreeOfNode(node):
    degree = app.crawler.getDegreeOfNode(int(node))
    return jsonify({"result": degree})

@app.route("/connectedNodesWithDegrees/<node>")
def connectedNodesWithDegrees(node):
    connectedNodes = app.crawler.getConnectedNodesWithDegrees(int(node))
    return jsonify({"result": connectedNodes})


class GraphServer:
    def __init__(self, graph, debug=False):
        # global
        app.debug = debug
        app.network = graph
        app.crawler = SnapGraphCrawler(graph)

    def run(self):
        app.run()

