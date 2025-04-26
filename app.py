# app.py

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

SOLR_URL = "http://localhost:8983/solr/lab11"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "")
    filter_query = request.args.get("fq", "")

    params = {
        "q": query or "*:*",
        "wt": "json",
        "rows": 10
    }
    if filter_query:
        params["fq"] = filter_query

    solr_response = requests.get(f"{SOLR_URL}/select", params=params).json()
    docs = solr_response["response"]["docs"]
    return jsonify(docs)

@app.route("/autocomplete")
def autocomplete():
    query = request.args.get("q", "")
    params = {
        "q": query,
        "wt": "json"
    }
    suggest_url = f"{SOLR_URL}/suggest"
    solr_response = requests.get(suggest_url, params=params).json()
    suggestions = solr_response.get("suggest", {})
    output = []
    for key in suggestions:
        for entry in suggestions[key][query]["suggestions"]:
            output.append(entry["term"])
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
