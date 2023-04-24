from flask import Flask,render_template,url_for,request,redirect,session
from functools import wraps
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import joblib
import pymongo

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
client = pymongo.MongoClient("mongodb+srv://jainilvk:1234qwer@cluster0.ibmkmor.mongodb.net/test")
db = client.test

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# Routes
from user import routes

@app.route('/')
def start():
    return render_template("index.html")

@app.route('/index.html')
def index():
    return render_template("index.html")


@app.route('/about.html',methods = ["POST","GET"])
def model():
    if request.method == 'POST':
        loaded_model = joblib.load('model_joblib')
        feature_list = request.form.to_dict()
        feature_list = list(feature_list.values())
        feature_list = list(map(float, feature_list))
        final_feature_list = np.array(feature_list)
        final_feature_list = final_feature_list.reshape(1,5)
        final = loaded_model.predict(final_feature_list)
        final = round(float(final),2)
        return render_template('about.html', prediction_text= ' {}$'.format(final))
    if request.method == 'GET':
        return render_template('about.html')


@app.route('/login.html',methods=["POST","GET"])
def log():
    return render_template("login.html")


@app.route('/welcome.html',methods=["POST","GET"])
def welcome():
    return render_template("welcome.html")

if (__name__) == '__main__':
    app.run(debug=True)

