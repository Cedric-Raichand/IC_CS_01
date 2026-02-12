from flask import Flask, render_template, request
from scanner import fetch_website
from report import generate_report

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    report = None

    if request.method == "POST":
        url = request.form.get("url")
        if url:
            result = fetch_website(url)
            report = generate_report(result)

    return render_template("index.html", result=result, report=report)

if __name__ == "__main__":
    app.run(debug=True)
