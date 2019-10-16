# -*- coding:utf-8 -*-

from app import app, db, auth
from flask import render_template, json, jsonify, request, abort, g, make_response
from app.models import *
from flask_cors import CORS
from utils import WriteLog

@app.route('/devops/api/v1.0/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username })

@auth.verify_password
def verify_password(username_or_token, password):
    username_token = request.headers.get('token')
    user = User.verify_auth_token(username_token)  
    if not user:
        return False    
    g.user = user   
    return True


@app.route('/devops/api/v1.0/login',methods=['POST'])
def get_auth_token(): 
    username = request.json.get('username') 
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user=user	
    WriteLog('api').info('user  is login')
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })
