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
from django.utils.html import escape as htmlspecialchars

from profanity_filter import ProfanityFilter

class Message():

    def __init__(self,messageIN,censorChar='•'):

        self.message = messageIN
        self.filter = ProfanityFilter()
        self.filter.censor_char = censorChar


    # Handle HTML Special Chars
    # Stop XSS injects
    def makeSafe(self):

        # Time is converted from UNIX timestamp into readable format
        self.message['time'] = datetime.utcfromtimestamp(int(self.message['time']) / 1000).strftime('%Y-%m-%d %H:%M:%S') 

        message = self.message['msg'][:1000]   

        #message = message.replace('<','&lt;') # Replace < with html safe < 
        #message = message.replace('>','&gt;') # Replace > with html safe > 
        #message = message.replace('<','&lt;') # Replace < with html safe < 
        #message = message.replace('>','&gt;') # Replace > with html safe > 

        message = htmlspecialchars(message)

        message = message.replace('\n','<br>')  
        message = message.replace(' ','&nbsp;')
        message = message.replace('\t','&Tab;') 

        self.message['msg'] = message


    # Formats links as <a> tags
    def formatLinks(self):

        message = '' #

        for word in self.message['msg'].split(' '): 

            if word[0:4] == 'http':
                message += f'<a href="{word}">{word}</a> ' 

            else: 
                message += word + ' ' 

        self.message['msg'] = message 


    # Removes illegals characters not defined in legalchars
    def legalize(self,legalchars):

        message = ''

        for char in self.message['msg'][:-1]: 

            if char not in legalchars: 
                message += '&diams;' 

            else:
                message += char 

        self.message['msg'] = message 

        username = ''

        for char in self.message['username']:

            if char not in legalchars: 
                username += '&diams;'

            else:
                username += char

        self.message['username'] = username 


    # Censors restricted words
    def censor(self,restrictedwords):

        self.message['msg'] = self.filter.censor(self.message['msg'])

        self.message['username'] = self.filter.censor(self.message['username'])

        for word in restrictedwords: 

            self.message['username'] = re.sub(word, self.filter.censor_char * len(word), self.message['username'], flags=re.IGNORECASE)  

            self.message['msg'] = re.sub(word, self.filter.censor_char * len(word), self.message['msg'], flags=re.IGNORECASE)  


    # Searches and replaces text
    def searchReplace(self,tags):

        for search,replace in tags:  

            self.message['msg'] = self.message['msg'].replace(search,replace) 
            self.message['username'] = self.message['username'].replace(search,replace) 


    # Image handling :
    # - Encoding
    # - Saving
    # - URLFOR
    # - Transfer
    def formatImg(self):

        if self.message['src'] != 'NOIMAGE':

            src = self.message['src'].split(',')
            data = src[1]
            ext = ((src[0].split('/'))[1].split(';'))[0]

            filename = f'upl/{self.message["time"]}.{ext}'
            with open('static/' + filename, 'wb') as f:
                f.write(base64.decodebytes(data.encode("ascii")))

            self.message['src'] = url_for("static", filename=filename)


    # Incase of admin tag
    # Kinda deprecated
    def tag(self, tagr, tagl):

        self.message['msg'] = self.message['msg'].replace(tagl,'<')
        self.message['msg'] = self.message['msg'].replace(tagr,'>')

