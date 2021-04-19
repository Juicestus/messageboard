#!/usr/bin/env python3

# Avert Server
# (c) Justus Languell 2020-2021

from flask import url_for

def loadAds():

    ads = []
    for l in open('ADVERTS','r'):
        if '@' in l:
            l = l.split('@')

            if l[1] == 'web':
                url = l[2]
            else:
                url = url_for("static", filename=f'ads/{l[2]}')
            ads.append((l[0],url))
    return ads