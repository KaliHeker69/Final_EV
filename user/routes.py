from flask import Flask
from app import app
from user.log import User

@app.route('/login.html', methods=['POST'])

def login():
  return User().login()
