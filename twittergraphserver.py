import networksize
from flask import Flask
from flask import jsonify

app = Flask(__name__)
# app.debug = True
network = None
crawler = None

# Twitter network sample
# 41.7 million user profiles, 1.47 billion social relations
importer = networksize.GraphImporter("/Users/balazs/Desktop/twitter_rv.net", 4561230)
network = importer.importGraph(False, 1000000)
crawler = networksize.SnapGraphCrawler(network)

@app.route("/")
def index():
    info = {"nodes":network.GetNodes(), "edges":network.GetEdges()}
    return jsonify({"result": info})

@app.route("/randomNode")
def randomNode():
    node = crawler.getRandomNode()
    return jsonify({"result": node})

@app.route("/highestDegreeNode")
def highestDegreeNode():
    node = crawler.getHighestDegreeNode()
    return jsonify({"result": node})

@app.route("/connectedNodes/<node>")
def connectedNodes(node):
    connectedNodes = crawler.getConnectedNodes(int(node))
    return jsonify({"result": connectedNodes})

@app.route("/degreeOfNode/<node>")
def degreeOfNode(node):
    degree = crawler.getDegreeOfNode(int(node))
    return jsonify({"result": degree})

if __name__ == '__main__':
    app.run()