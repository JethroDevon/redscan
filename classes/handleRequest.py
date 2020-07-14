#!/usr/bin/env python3
from loggingObject import LoggingObject
import unicodedata

#This class will handle some of the logic behind incoming user input, sanitise incoming data for parameters 
class HandleRequest:
    
    def sanitise(request):
   
        request = request[request.find("/")+1:request.find("HTTP")]
        PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/_-=&" 
        request = "".join(c for c in request if c in PERMITTED_CHARS)     
        return request

    #seperates incoming parameters into a list of pairs
    def parameterise(parameters):

        for char in parameters:
            if char in "/?":
                parameters.replace(char,'')

        #create a key value tuple array out of incoming request 
        parameters = parameters.split("&")
        parameter_pairs = dict(string.split('=') for string in parameters)
        return parameter_pairs

    
    #if is a time query return parameters to call the function otherwise return False
    #def timeQuery(input):

     #   if(
