#!/usr/bin/env python3

# 2021 CSP Create Project
# A realtime internet chat room using WebSockets handled with Flask SocketIO
# Built on a Flask Python server with a JavaScript client

# Libraries Flask and Flask SocketIO must be installed using PIP, the Python Package Manager
# This project is designed to be ran on a UNIX system, tested on MacOSX 11 and Ubuntu 18.04 LTS

# Flask <https://flask.palletsprojects.com/en/1.1.x/>
# Flask SocketIO <https://flask-socketio.readthedocs.io/en/latest/>

from flask import Flask, render_template, url_for # Flask handles hosting of webserver                       # install with: pip install flask
from flask_socketio import SocketIO, emit         # Flask SocketIO handles WebSocket Interface               # install with: pip install flask_socketio
from datetime import datetime                     # Datetime handles dates and times                         # preinstalled
import re                                         # Regex handles advanced string search and replacment      # preinstalled
import sys                                        # Using to handle entry args                               # preintsalled

from profanity_filter import ProfanityFilter
import base64

# INITIAL VARS

restrictedwords = [] # Add words to be censored
imgnum = 1

# legal characters to display
legalchars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,./<>:?;\'"[]{}|-_=+!@#$%^&*()~≠±–—¡™£¢∞§¶• '

formatTags = [('**:','<b>'),('**','</b>'),('*:','<i>'),('*','</i>'),('#:','<code>'),('#','</code>')] 
# List of tuples of replacments for formating 

app = Flask(__name__,template_folder='html') # Get Flask App
socketio = SocketIO(app) # Setup Socket Enviorment with App

messages = list() # Instantiate list of messages


class Message():

    def __init__(self,messageIN,censorChar='•'):

        self.message = messageIN
        self.filter = ProfanityFilter()
        self.filter.censor_char = censorChar


    def makeSafe(self):

        # Time is converted from UNIX timestamp into readable format
        self.message['time'] = datetime.utcfromtimestamp(int(self.message['time']) / 1000).strftime('%Y-%m-%d %H:%M:%S') 

        message = self.message['msg'][:1000]    # Delete all the extra characters

        message = message.replace('<','&lt;') # Replace < with html safe < 
        message = message.replace('>','&gt;') # Replace > with html safe > 
        message = message.replace('<','&lt;') # Replace < with html safe < 
        message = message.replace('>','&gt;') # Replace > with html safe > 

        message = message.replace('\n','<br>')  # Replace \n with html safe <br>
        message = message.replace('\t','&Tab;') # Replace \t with html safe &Tab;

        self.message['msg'] = message


    def formatLinks(self):

        message = '' # New string for new message

        for word in self.message['msg'].split(' '): # Iterates through every word in message

            if word[0:4] == 'http': # If string starts with "http", meaning it's a link
                message += f'<a href="{word}">{word}</a> ' # Format it to render as an HTML link and add it into the new message

            else: # If not that
                message += word + ' ' # Just add it to the new message regular

        self.message['msg'] = message # Set the message to the new link formatted message


    def legalize(self,legalchars):

        message = '' # New string for new message

        for char in self.message['msg'][:-1]: # Itereate through every chracter in the message 

            if char not in legalchars: # if the character is not legal
                message += '&diams;' # Replace it with the unknown character symbol

            else: # If not
                message += char # Just leave it be

        self.message['msg'] = message # Set the message to the new link formatted message

        username = '' # New string for new message

        for char in self.message['username']: # Itereate through every chracter in the message 

            if char not in legalchars: # if the character is not legal
                username += '&diams;' # Replace it with the unknown character symbol

            else: # If not
                username += char # Just leave it be

        self.message['username'] = username # Set the message to the new link formatted message

    def censor(self,restrictedwords):

        self.message['msg'] = self.filter.censor(self.message['msg'])

        self.message['username'] = self.filter.censor(self.message['username'])

        for word in restrictedwords:  # Iterates through words to censor

            # Replaces them in the username, case insensitive because of regex
            self.message['username'] = re.sub(word, self.filter.censor_char * len(word), self.message['username'], flags=re.IGNORECASE)  

            # Replaces them in the message, case insensitive because of regex
            self.message['msg'] = re.sub(word, self.filter.censor_char * len(word), self.message['msg'], flags=re.IGNORECASE)  


    def searchReplace(self,tags):

        for search,replace in tags:  # Iterates through the search and replaces of list of tuples: fontTags

            # Replaces the search with the replace, for bold, italic, and code formating
            self.message['msg'] = self.message['msg'].replace(search,replace) 
            self.message['username'] = self.message['username'].replace(search,replace) 

    def formatImg(self):

        if self.message['src'] != 'NOIMAGE':

            src = self.message['src'].split(',')
            data = src[1]
            ext = ((src[0].split('/'))[1].split(';'))[0]

            filename = f'upl/{self.message["time"]}.{ext}'
            with open('static/' + filename, 'wb') as f:
                f.write(base64.decodebytes(data.encode("ascii")))

            self.message['src'] = url_for("static", filename=filename)



# SOCKETIO EVENTS
@socketio.event                                 
def updateMessage(message):                         # Message comes in from client as param "message"

    message = Message(message)                      # Instantiate the message as an instance of our class

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



# ENTRY POINT
if __name__ == '__main__':

    if '-d' in sys.argv:
        socketio.run(app,debug=True)          # Run SocketIO App and Async subprocesses in debug mode

    else:
        socketio.run(app,host='0.0.0.0',port=80,debug=False) # Run App on port 80 for production