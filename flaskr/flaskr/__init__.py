import os
import io
from flaskr import ONS
import flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,FloatField
from wtforms.validators import InputRequired
#from flask_json import FlaskJSON, JsonError, json_response, as_json
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from flask import Flask, send_file, make_response,request
from flask import jsonify
import requests
import json

API_URL = "http://127.0.0.1:5000/api/"

# create and configure the app
app = flask.Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    SECRET_KEY='dev',
)
#json = FlaskJSON(app)
"""FlaskJSON(app)
if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
"""
class Formula(FlaskForm):
    formula = StringField("formuła matematyczna")
    start=FloatField("start")
    stop=FloatField("stop")
    step=FloatField("krok")
    submit = SubmitField("Zamień")   
     
@app.route('/ONP',methods=['GET','POST'])
def ONP():
    form = Formula()
    if form.validate_on_submit():
       #return flask.redirect(flask.url_for("zmien_notacje"))
       #return flask.redirect(flask.url_for("wykres2",R=form.formula._value(),start=float(form.start._value()),stop=float(form.stop._value()),step=int(form.step._value())))
       #return data_to_JSON(R=form.formula._value(),start=float(form.start._value()),stop=float(form.stop._value()),step=int(form.step._value()))
       data_to_JSON(R=form.formula._value(),start=float(form.start._value()),stop=float(form.stop._value()),step=int(form.step._value()))
       return wykres2()
       #return wykres2(R=form.formula._value(),start=float(form.start._value()),stop=float(form.stop._value()),step=int(form.step._value()))
       #return flask.redirect(flask.url_for("data_to_JSON",R=form.formula._value(),start=float(form.start._value()),stop=float(form.stop._value()),step=int(form.step._value())))
    return flask.render_template('index.html',form=form)
  
@app.route('/wynik',methods=['GET'])
def zmien_notacje():
    R=flask.session["R"]
    start= flask.session["start"]
    stop= flask.session["stop"]
    step=flask.session["krok"]
    S='Odwrotna Notacja Polska:' +''.join([str(elem) for elem in R])
    bytes_object=wykres(R,start,stop,step,S)
    #return flask.render_template('wynik.html')
    return send_file(bytes_object,attachment_filename='plot.png',  mimetype='image/png')

#@app.route('/wykres2/<R>/<float:start>/<float:stop>/<int:step>', methods=['GET'])
#def wykres2(R,start,stop,step):
@app.route('/wykres2', methods=['GET'])
def wykres2():
    r = request.get_json(force=True)
    R=r["R"]
    start= r["start"]
    stop= r["stop"]
    step=r["step"]
    _x=np.linspace(start,stop,step)
    x = [_ for _ in _x ]
    R=ONS.ONP(ONS.string_to_tokens(R))
    y=ONS.multiple_calculations(start,stop,step,R)
    S='Odwrotna Notacja Polska:' +''.join([str(elem) for elem in R])
    return flask.render_template("plot.html", x=x, y=y,S=S)

@app.route('/wykres',methods=['GET','POST'])
def wykres(R,start,stop,step,S):
     x=np.linspace(float(start),float(stop),float(step))
     y=ONS.multiple_calculations(float(start),float(stop),int(step),R)
     fig,ax=plt.subplots()
     ax.plot(x,y,'o-')
     ax.grid(True)
     plt.title(S)
     ax.tick_params(labelcolor='r', labelsize='medium', width=3)
     bytes_image = io.BytesIO()
     plt.savefig(bytes_image, format='png')
     bytes_image.seek(0)
     return bytes_image
     #return send_file(bytes_image,attachment_filename='plot.png',mimetype='image/png')


class TransformForm(FlaskForm):
    formula = StringField("formuła matematyczna", validators=[InputRequired()])
    submit = SubmitField("Zamień")  


@app.route('/api/tokens',methods=["GET"])
def tokens():
    try:
        formula = request.args.get('formula')
        R=ONS.ONP(ONS.string_to_tokens(formula))
        return jsonify({"status" : "ok", "result": { "rpn" : R}})
    except Exception as ex:
        return jsonify({ "status" : "error", "message" : str(ex) })
    
@app.route('/transform', methods=['GET', 'POST'])
def transform():
    try:
        form = TransformForm()
        if form.validate_on_submit():
            formula = form.formula._value()
            r = requests.get(API_URL + "tokens?formula="+formula)
            j = json.loads(r.text)
            return flask.render_template("transform_result.html", formula=formula, result=j['result']['rpn'])
        return flask.render_template("transform.html", form=form)
    except Exception as ex:
        return flask.render_template("transform.html", form=form)