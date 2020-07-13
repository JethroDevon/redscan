#!/usr/bin/env python3
import socketserver
from loggingObject import LoggingObject



# This class contains the functionality for the restful server, it will also be responsible for validating incoming data
class ServerObject(socketserver.BaseRequestHandler):

       #OVERIDE: Each incoming connection is handled here 
       def handle(self):
              
        # self.request is the TCP socket connected to the client
        self.rawdata = self.request.recv(1024).strip()
        LoggingObject("Connection", "connection to: " + format (self.client_address[0]))
        
        self.request.sendall(self.rawdata)
