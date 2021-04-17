#!/usr/bin/env python3

# Main server file
# (c) Justus Languell 2020-2021

from message import Message 
from user import UsersRepository, User

from flask import Flask, render_template, url_for, request, abort, redirect, Response
from flask_socketio import SocketIO, emit         
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user

from datetime import datetime                     
import re                                         
import sys                                        

from profanity_filter import ProfanityFilter
import base64

from threading import Lock, Thread
from time import sleep
from hashlib import sha256

messages = list() 

restrictedwords = [] 
imgnum = 1

legalchars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,./<>:?;\'"[]{}|-_=+!@#$%^&*()~≠±–—¡™£¢∞§¶•\   '
formatTags = [('**:','<b>'),(':**','</b>'),('*:','<i>'),(';*','</i>'),('#:','<code>'),(':#','</code>'),(':::','<code>'),(';;;','</code>')] 

secretKey = 'secret_key'

app = Flask(__name__,template_folder='html') 
app.config['SECRET_KEY'] = secretKey
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
socketio = SocketIO(app) 

users_repository = UsersRepository()

def sha(s):
    return sha256(bytes(s,'utf-8')).hexdigest()

@app.route('/')
@login_required
def index():
    
    return render_template('index.html', currentUser = current_user.username)   

@socketio.event                                 
def connected():                                 

    emit('newMessage',messages,broadcast=True)  


@socketio.event                                 
def updateMessage(message):                         

    message = Message(message)                      

    message.formatImg()
    message.makeSafe()
    message.searchReplace(formatTags)                             
    message.formatLinks()
    message.legalize(legalchars)
    message.censor(restrictedwords)

    messages.append(message.message)

    emit('newMessage',messages,broadcast=True)   


@app.route('/login' , methods=['GET' , 'POST'])
def login():

    serverError = ''

    if request.method == 'POST':

        username = request.form['username']
        password = sha(username + request.form['password'])

        registeredUser = users_repository.get_user(username)

        if registeredUser != None and registeredUser.password == password:

            login_user(registeredUser)
            return redirect('/')

        else:
            serverError = 'Login Failed: Cannot find user and password combination! Sign Up?'

    return render_template('login.html',serverError=serverError)


@app.route('/signup' , methods = ['GET' , 'POST'])
def register():
    serverError = ''

    if request.method == 'POST':

        username = request.form['username']
        password = sha(username + request.form['password'])
        confirm = sha(username + request.form['confirm'])

        if password == confirm:

            if username not in users_repository.list_users():

                new_user = User(username , password , users_repository.next_index())
                users_repository.save_user(new_user)

                login_user(new_user)
                return redirect('/')

            else:
                serverError = 'Signup Failed: Username Already Registered!'
        else:
            serverError = 'Signup Failed: Password Do Not Match!'

    return render_template('signup.html',serverError=serverError)
  

@app.errorhandler(404)
def Not_Found(e):

    err = str(e).split(':')
    return render_template('error.html',err=err[0],info=err[1])


@app.errorhandler(401)
def Unauthorized(e):

    err = str(e).split(':')
    return render_template('error.html',err=err[0],info=err[1])


@app.errorhandler(403)
def Forbidden(e):

    err = str(e).split(':')
    return render_template('error.html',err=err[0],info=err[1])


@app.errorhandler(400)
def Bad_Request(e):

    err = str(e).split(':')
    return render_template('error.html',err=err[0],info=err[1])


@app.errorhandler(418)
def teapot(e):

    err = str(e).split(':')
    return render_template('error.html',err=err[0],info=err[1])


@app.errorhandler(500)
def Internal_Server_Error(e):

    err = str(e).split(':')
    return render_template('error.html',err=err[0],info=err[1])


@login_manager.user_loader
def load_user(userid):

    r = users_repository.get_user_by_id(userid)
    return r


@app.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect('/')

if __name__ == '__main__':

    #if not '-t' in sys.argv:
        #runThreads()

    if '-d' in sys.argv:
        socketio.run(app,debug=True)         

    else:
        socketio.run(app,host='0.0.0.0',port=80,debug=False) 
