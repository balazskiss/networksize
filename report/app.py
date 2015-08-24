__author__ = 'balazs'

from flask import Flask
from flask import jsonify, redirect
import glob
import os
import csv

def csv_to_array(csvfile):
    fields = None
    objects = []
    f = open(csvfile, 'rt')
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
            objects.append(obj)
    finally:
        f.close()
    return objects

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
    file = "../"+file
    if file.endswith(".csv"):
        content = csv_to_array(file)
    else:
        with open(file, 'r') as content_file:
            content = content_file.read()
    return jsonify({"result": content})

if __name__ == "__main__":
    app.run()