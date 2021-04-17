#!/usr/bin/env python3

# User Classes
# (c) Justus Languell 2020-2021


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


class User(UserMixin):

    def __init__(self , username , password , id , active=True):

        self.id = id
        self.username = username
        self.password = password
        self.active = active


    def get_id(self):

        return self.id


    def is_active(self):

        return self.active


    def get_auth_token(self):

        return make_secure_token(self.username , key='secret_key')


class UsersRepository:

    def __init__(self):

        self.users = dict()
        self.users_id_dict = dict()
        self.identifier = 0
    
    def save_user(self, user):

        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)
    
    def get_user(self, username):

        return self.users.get(username)
    
    def get_user_by_id(self, userid):

        return self.users_id_dict.get(userid)
    
    def next_index(self):

        self.identifier +=1
        return self.identifier

    def list_users(self):
        
        return list(self.users.keys())