#!/usr/bin/env python3
import ssl, socket, sys
from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
from loggingObject import LoggingObject
from handleRequest import HandleRequest
from db import DB

#once initialised incoming data will be ha
class ServerObject():
  
      #Wraps a socket object to handle TLS, arguments are host address, port to access and path to SSL key files
      def __init__(self, addr, port, certpath, database_url):  

           self.req = HandleRequest
           self.sock = socket.socket()
           self.sock.bind((addr, port))
           self.sock.listen(5)
           self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
           self.context.load_cert_chain(certfile=(certpath + "cert.pem"), keyfile=(certpath + "key.pem"))
           self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
           self.context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
           LoggingObject("INIT", "SSL server created")
           self.db = DB(database_url); # initialising the database object with the url of the hosted csv file

      def reply(self, connection, response):

            if(len(response[0]) <= 1):
                  connection.write(('HTTP/1.1 200 OK\n\n%s' % response).encode())

            else:
                  multi_response = ""
                  for row in response:
                        multi_response += (str(row) + "\n")

                  connection.write(('HTTP/1.1 200 OK\n\n%s' % multi_response).encode())
                  
      #this function will handle and incoming request and respond appropriately
      def handle(self, control_message):

               if(control_message != ""):
                  print("place holder for something")
                  
               try:
                     
                   #initiallise conn when next connection is made
                   conn = None
                   ssock, addr = self.sock.accept()
                   conn = self.context.wrap_socket(ssock, server_side=True)
                   recieved = str(conn.recv(4096))
                   LoggingObject("REQUEST", recieved)

                   #parse arguments from connection to get list of commands and thier parameters for database operations
                   parameters = self.req.parameterise(self.req.sanitise(recieved))

                   #prepare to return a string containing the response from the database
                   response = "NOT FOUND"
                   
                   if("authuser" in parameters and "passwordhash" in parameters):                  
                       response = self.db.usertokenRequest(parameters.get("authuser"),parameters.get("passwordhash"))
                         
                   #if user and token exist
                   elif("username" in parameters and "token" in parameters):

                       #if credentials allow user to use database queries
                       can_access = self.db.checkToken(parameters.get("username"),parameters.get("token"))

                       print("access allowed?" + str(can_access))
                       if(parameters.get("command") == "time_range" and can_access):
                           if "start_time" in parameters and "end_time" in parameters:
                               response = self.db.timeRequest(parameters.get("start_time"),parameters.get("end_time"))
                         
                       elif(parameters.get("command") == "request" and can_access):
                           if "column" in parameters and "value" in parameters:
                               response = self.db.standardRequest(parameters.get("column"), parameters.get("value"))        

                       elif(parameters.get("command") == "tableinfo" and can_access):
                           response = self.db.tableInfo()

                       elif(parameters.get("command") == "markRead" and can_access):
                           if "id" in parameters and "status" in parameters:
                               response = self.db.setURead(parameters.get("id"), parameters.get("status"))
                   
                   self.reply(conn, response)
                   parameters = ""
                   recieved = ""
                  
               except ssl.SSLError as e:
                   LoggingObject("ERROR", str(e))
               
               except Exception as e:
                   LoggingObject("ERROR", "handling query: " + str(e))

               
              
      def close():
            LoggingObject("CLOSE","closing service")
            conn.close()
                              


                   
        
