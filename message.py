#!/usr/bin/env python3

# Message Class File
# (c) Justus Languell 2020-2021

# I know i already imported these but fuck you!
from flask import Flask, render_template, url_for 
from flask_socketio import SocketIO, emit         
from datetime import datetime                     
import re                                         
import sys                                        
import base64

class Message():

    def __init__(self,messageIN,PF,censorChar='•'):

        self.message = messageIN
        self.filter = PF
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

    def tag(self, tagr, tagl):

        self.message['msg'] = self.message['msg'].replace(tagl,'<')
        self.message['msg'] = self.message['msg'].replace(tagr,'>')

# sexy class go brrrrr
