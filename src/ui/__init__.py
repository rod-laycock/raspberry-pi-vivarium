# /flask_2/__init__.py
from flask import Flask, render_template, Response

app = Flask(__name__)
app.debug = True

@app.route("/", methods=["GET"], )
def get_home():

  return render_template('index.html')
  #return Response("Vivarium Monitoring Website Application up and running.", status=200, mimetype="text/html")