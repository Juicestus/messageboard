#!/usr/bin/env python3

# Main server file
# (c) Justus Languell 2020-2021

from message import Message 

from flask import Flask, render_template, url_for 
from flask_socketio import SocketIO, emit         
from datetime import datetime                     
import re                                         
import sys                                        

from profanity_filter import ProfanityFilter
import base64

from threading import Lock, Thread
from time import sleep


# INITIAL VARS

messages = list() 

restrictedwords = [] # Add words to be censored
imgnum = 1


threads = []

def pruner():

    print('Pruner thread loop goes here')

threads.append(Thread(target=pruner))


# This doesnt need to exist anymore bc i fixed the root problem
# requring this seperate statement, but im too lazy to delete it
# in the other file so ima just leave this part /:
PF = ProfanityFilter()

legalchars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,./<>:?;\'"[]{}|-_=+!@#$%^&*()~≠±–—¡™£¢∞§¶•\   '

formatTags = [('**:','<b>'),(':**','</b>'),('*:','<i>'),(';*','</i>'),('#:','<code>'),(':#','</code>'),(':::','<code>'),(';;;','</code>')] 

app = Flask(__name__,template_folder='html') 
socketio = SocketIO(app) 

# Ignore this
def jesus(tag):
    jesus = url_for("static", filename="img/jesus.gif")
    style = '''<style>
    body {
        background-color: black;
    }
    img {
        margin:20px;
    }
    h1 {
        color: white;
        font-family: arial;
    }
    </style>'''
    return f'''{style}<h1>{tag} coming soon!</h1>
    <img style="" src="{jesus}" max-width="600px;">'''

# SOCKETIO EVENTS
@socketio.event                                 
def updateMessage(message):                         

    message = Message(message, PF)                      

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
def index():            

    return render_template('index.html')         

@app.route('/login',methods=['GET','POST'])
def login():

    return jesus('Login')

@app.route('/signup',methods=['GET','POST'])
def signup():

    return jesus('Signup')


def runThreads():

    for thread in threads:
        thread.daemon = True
        thread.start()


# ENTRY POINT
if __name__ == '__main__':

    if not '-t' in sys.argv:
        runThreads()

    if '-d' in sys.argv:
        socketio.run(app,debug=True)         

    else:
        socketio.run(app,host='0.0.0.0',port=80,debug=False) # Run App on port 80 for production


# THIS SOMEHOW ALL WORKS WTF!!!
# I am the most based coder yes.
