from flask import Flask,render_template, request


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():

    return render_template("index.html")


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
