import logging
from flask import Flask, Flask, render_template, request, jsonify
from flask_googlemaps import GoogleMaps
from wtforms import SelectField
from flask_wtf import FlaskForm
# from pysal_test import cluster
from map import mapper
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'Circe2635!',
    'db': 'zoovision',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation

db = SQLAlchemy(app)


class Form(FlaskForm):
    factor = SelectField('state', choices=['POP2000', 'POP2010'])


@app.route("/", methods=['GET', 'POST'])
def home():
    file = "C:\zoovision\data\states\states2.shp"
    title = "United States"
    result = mapper(file, title)
    return render_template("home.html", result=result)


@app.route("/surveillance", methods=['GET', 'POST'])
def surveillance():
    file = "C:\zoovision\data\states\states2.shp"
    title = "United States"
    result = mapper(file, title)
    viruses = ['West Nile Virus', 'Influenza H1N1', 'Influenza H2N1']
    # form= Form()
    # form.factor
    risk_factors = ['POP2000', 'POP2010']
    return render_template("surveillance.html", viruses=viruses, risk_factors=risk_factors, result=result)


@app.route("/survey", methods=['GET', 'POST'])
def survey():
    states = "C:\zoovision\data\states\states.shp"
    title = "United States"
    view = mapper(states, title)
    return render_template("survey.html", view=view)


@app.route("/prediction_analysis", methods=['GET', 'POST'])
def prediction_analysis():
    return render_template("prediction_analysis.html")


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
