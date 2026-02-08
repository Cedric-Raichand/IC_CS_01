from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/scan', methods=['POST'])
def scan():
    url = request.form.get("url")
    return f"You entered: {url}"


if __name__ == '__main__':
    app.run(debug=True)
