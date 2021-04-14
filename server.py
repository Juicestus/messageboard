#!/usr/bin/env python3

# Main server file
# (c) Justus Languell 2020-2021

from message import Message 
#from user import DataBase, User

from flask import Flask, render_template, url_for, request, abort, redirect, Response
from flask_socketio import SocketIO, emit         
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user

from datetime import datetime                     
import re                                         
import sys                                        

from profanity_filter import ProfanityFilter
import base64

from threading import Lock, Thread
from time import sleep


threads = []

def pruner():

    print('Pruner thread loop goes here')

threads.append(Thread(target=pruner))



# User classes and methods
# Move to User.py

class User(UserMixin):

    def __init__(self, username, password, id, active=True):

        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def getId(self):

        return self.id

    def isActive(self):

        return self.active

    def getAuthToken(self):

        return make_secure_token(self.username, keys=secretKey)


class Users:

    def __init__(self):

        self.users = {}
        self.userIDs = {}
        self.identifier = 0

    def saveUser(self, user):

        self.userIDs.setdefault(user.id, user)
        self.users.setdefault(user.username, user)

    def getUser(self, username):

        return self.users.get(username)

    def getUsersByID(self, userid):

        return self.userIDs.get(userid)

    def nextIndex(self):

        self.identifier +=1
        return self.identifier

    def listUsers(self):

        return list(self.users.keys())



messages = list() 
users = Users()

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


@app.route('/login',methods=['GET','POST'])
def login():

    note = ''

    print(users.listUsers())
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        registeredUser = users.getUser(username)

        if registeredUser != None and registeredUser.password == password:
            return redirect('/')
        else:
            note = '<p style="color: red;">Login Failed: User Not Found!</p><a href="signup">Sign Up?</a>'
        #return redirect(url_for('home'))
        
    
    return Response(f'''
        <h1>Login</h1>
        <p>Don't have an account? <a href="signup">Sign Up?</a></p>
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        {note}
        ''')
        

@app.route('/signup',methods=['GET','POST'])
def signup():
    
    note = ''

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        if password == confirm:

            if username not in users.listUsers():

                newUser = User(username, password, users.nextIndex())

                users.saveUser(newUser)

                return redirect('/')

            else:
                note = '<p style="color: red;">Signup Failed: Username Already Registered!</p>'

        else:
            note = '<p style="color: red;">Signup Failed: Password Do Not Match!</p>'


    return Response(f'''
        <h1>Sign Up</h1>
        <form action="" method="post">
        <p><input type=text name=username placeholder="Enter username">
        <p><input type=password name=password placeholder="Enter password">
        <p><input type=password name=confirm placeholder="Confirm password">
        <p><input type=submit value=Register>
        </form>
        {note}
        ''') 

@app.errorhandler(401)
def loginFailed(e):
    return Response('<p>Login Failed!</p>')


@app.errorhandler(404)
def pageNotFound(e):
    return Response('<p>Page Not Found!</p>')


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


@socketio.event                                 
def connected():                                 

    emit('newMessage',messages,broadcast=True)  

# ROUTES
@app.route('/',methods=['GET'])     
#@login_required        
def index():            

    try:
        cuser = current_user.username
    except AttributeError:
        cuser = 'Guest'

    return render_template('index.html', currentUser = cuser)         

@login_manager.user_loader
def loadUser(userid):
    return users.getUsersByID(userid)


def runThreads():

    for thread in threads:
        thread.daemon = True
        thread.start()


if __name__ == '__main__':

    if not '-t' in sys.argv:
        runThreads()

    if '-d' in sys.argv:
        socketio.run(app,debug=True)         

    else:
        socketio.run(app,host='0.0.0.0',port=80,debug=False) 

