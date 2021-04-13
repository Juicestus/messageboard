#!/usr/bin/env python3

# Main server file
# (c) Justus Languell 2020-2021

from message import Message # plz dont cause name issues if u do ill cry

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


messages = list() # Instantiate list of messages

restrictedwords = [] # Add words to be censored
imgnum = 1

# add here a thread to prune the messages and images 
# storage system based in hard memory. 
# Or dont be a cuck and do it now.
# or not...

# it doesnt work im about to cry


threads = []

def pruner():

    print('rn this thread dont do nothin')
    '''    
    while True:
        #messages = messages[1:]
        try:
            messages = messages[-3:]
        except:
            print('exception')
        sleep(5)
    '''

threads.append(Thread(target=pruner))


# This doesnt need to exist anymore bc i fixed the root problem
# requring this seperate statement, but im too lazy to delete it
# in the other file so ima just leave this part /:
PF = ProfanityFilter()

# legal characters to display
legalchars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,./<>:?;\'"[]{}|-_=+!@#$%^&*()~≠±–—¡™£¢∞§¶• '

formatTags = [('**:','<b>'),('**','</b>'),('*:','<i>'),('*','</i>'),('#:','<code>'),('#','</code>')] 
# List of tuples of replacments for formating 

app = Flask(__name__,template_folder='html') # Get Flask App
socketio = SocketIO(app) # Setup Socket Enviorment with App



# SOCKETIO EVENTS
@socketio.event                                 
def updateMessage(message):                         # Message comes in from client as param "message"

    message = Message(message, PF)                      # Instantiate the message as an instance of our class

    message.formatImg()
    message.makeSafe()                              # Comment this part out later u lazy fuck
    message.formatLinks()
    message.legalize(legalchars)
    message.censor(restrictedwords)
    message.searchReplace(formatTags)

    messages.append(message.message)

    emit('newMessage',messages,broadcast=True)   # List of messages is sent to all the clients to be updated


@socketio.event                                 
def connected():                                 # On client connection

    emit('newMessage',messages,broadcast=True)   # Send current messages to client

# ROUTES
@app.route('/',methods=['GET'])                                        
def index():            

    return render_template('index.html')         # Serves index.html

@app.route('/login',methods=['GET','POST'])
def login():

    return '''<h1>Login coming soon!</h1>
    img style="margin:20px;" src='{{ url_for("static", filename="img/jesus.gif") }}' max-width="600px;">'''


@app.route('/signup',methods=['GET','POST'])
def signup():

    return '''<h1>Signup coming soon!</h1>
    img style="margin:20px;" src='{{ url_for("static", filename="img/jesus.gif") }}' max-width="600px;">'''

def runThreads():

    for thread in threads:
        thread.daemon = True
        thread.start()


# ENTRY POINT
if __name__ == '__main__':

    if not '-t' in sys.argv:
        runThreads()

    if '-d' in sys.argv:
        socketio.run(app,debug=True)          # Run SocketIO App and Async subprocesses in debug mode

    else:
        socketio.run(app,host='0.0.0.0',port=80,debug=False) # Run App on port 80 for production


# THIS SOMEHOW ALL WORKS WTF!!!
# I am the most based coder yes.
