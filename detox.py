#!/usr/bin/env python3

# Detoxify Wrapper
# (c) Justus Languell 2020-2021


from detoxify import Detoxify
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def toxicScore(s):

    result = Detoxify('original').predict(s)
    scores = []
    metric = result
    for key in result.keys():
        scores.append(result[key])
        metric[key] = int(round(metric[key] * 1000))
    
    return max(scores), metric, result

