#!/usr/bin/env python3
from loggingObject import LoggingObject
import unicodedata

#This class will sanitise incoming data,
class HandleRequest:
        
    def sanitise(request):
   
        request = request[request.find("/")+1:request.find("HTTP")]
        PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-=&" 
        request = "".join(c for c in request if c in PERMITTED_CHARS)
        
        return request
