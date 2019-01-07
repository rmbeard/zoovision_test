import logging
from model import InputForm
from compute import compute
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    # mapped = mapper()
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        result = compute(form.A.data, form.b.data,
                         form.w.data, form.T.data)
    else:
        result = None

    return render_template("home.html", form=form, result=result)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
