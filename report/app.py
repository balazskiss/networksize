__author__ = 'balazs'

from flask import Flask
from flask import jsonify, redirect
import glob
import os
import csv

app = Flask(__name__, static_url_path='')
app.debug = True

@app.route('/')
def index():
    return redirect("/index.html")

@app.route("/files")
def files():
    files = glob.glob("../*.csv")
    for i in range(0, len(files)):
        files[i] = os.path.basename(files[i])
    return jsonify({"result": files})

@app.route("/files/<file>")
def file(file):
    fields = None
    content = []
    f = open("../"+file, 'rt')
    try:
        reader = csv.reader(f)
        for row in reader:
            if fields == None:
                fields = row
                continue
            obj = {}
            for i in range(0, len(fields)):
                field = fields[i]
                obj[field] = row[i]
            content.append(obj)
    finally:
        f.close()
    return jsonify({"result": content})

if __name__ == "__main__":
    app.run()