# Created by Rachel Beard: last updated 1/11/19
# Purpose: This is the entry point for a flask application that serves to
# Zoovision, a spatial decision support web application
import logging
from flask import render_template,  request
# from flask_bootstrap import Bootstrap
from flask_nav import Nav
# from flask_nav.elements import Navbar, Subgroup, View, Link, Text
# from flask_googlemaps import GoogleMaps
# from wtforms import SelectField, SubmitField, Form, TextField, TextAreaField, validators
# from flask_wtf import FlaskForm
from map import maps1, sum_chart
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, session
# from db_setup import init_db

app = Flask(__name__)
# Bootstrap(app)
nav = Nav(app)

# nav.register_element('my_navbar', Navbar('thenav', View('Home', 'home')))

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Circe2635!@localhost/zoovision'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation
# app.secret_key = 'secret key'
#
# # Set up database
# engine = create_engine('postgresql://postgres:Circe2635!@localhost/zoovision', convert_unicode=True)
# db = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# db = SQLAlchemy(app)

# init_db()


@app.before_request
def session_management():
    # make the session last indefinitely until it is cleared
    session.permanent = True


@app.route("/", methods=['GET', 'POST'])
def home():
    file = "C:\zoovision\data\Export_Output.shp"
    # set defualt parametersx
    seasons = [ '2016-17', '2017-18', '2018-19']
    viruses = ['H1N1', 'H3N2']
    risk_factors = ['PERCENT POSITIVE', '%UNWEIGHTED ILI']
    week = ''
    if request.method == 'GET':
        session['selected_risk'] = "PERCENT POSITIVE"
        session['selected_season'] = '2015-16'
        session['selected_week'] = 1
        selected_risk = session['selected_risk']
        selected_season = session['selected_season']
        selected_week = session['selected_week']
    elif request.method == 'POST':
        if 'Query' in request.form:
            selected_season = request.form['season']
            # selected_virus = request.form['virus']
            selected_risk = request.form['risk_factor']
            session['selected_risk'] = selected_risk
            session['selected_season'] = selected_season
            selected_week = session['selected_week']
            print(selected_week)
            result = maps1(file, selected_risk, selected_season, selected_week)
            chart = sum_chart()
            return render_template("tab.html", week=week, min=40, max=52, selected_week=selected_week, seasons=seasons,
                                   selected_risk=selected_risk, selected_season=selected_season,
                                   viruses=viruses, risk_factors=risk_factors, result=result, chart=chart)
        elif 'hello' in request.form:
            selected_week = request.form['week']
            selected_week = int(selected_week)
            print(type(selected_week))
            if selected_week < 13:
                selected_val = selected_week + 40
            else:
                selected_val = selected_week -12
            selected_risk = session['selected_risk']
            selected_season = session['selected_season']
            session['selected_week'] = selected_week
            print(selected_week)
            result = maps1(file, selected_risk, selected_season, selected_val)
            chart = sum_chart()
            return render_template("tab.html", selected_week=selected_week, week=week, min=40, max=52, seasons=seasons,
                                   selected_risk=selected_risk, selected_season=selected_season, viruses=viruses, risk_factors=risk_factors,
                                   result=result, chart=chart)
    # chart = sum_chart(selected_risk, selected_season)
    result = maps1(file, selected_risk, selected_season, selected_week)
    #result = "C:\zoovision\static\default.png"
    chart = sum_chart()
    return render_template("tab.html", week=week, min=40, max=52, seasons=seasons, selected_week=selected_week,
                           selected_risk=selected_risk, selected_season=selected_season, viruses=viruses,
                           risk_factors=risk_factors,
                           result=result, chart=chart)




if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
