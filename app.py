from flask import Flask, render_template, request
from scanner import fetch_website
from report import generate_report
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    report = None
    timestamp = None

    if request.method == "POST":
        url = request.form.get("url")
        if url:
            result = fetch_website(url)
            report = generate_report(result)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render_template("index.html", result=result, report=report, timestamp=timestamp)


if __name__ == "__main__":
    app.run(debug=True)
