#!/usr/bin/env python3
import ssl, socket, sys
from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
from loggingObject import LoggingObject
from handleRequest import HandleRequest

#once initialised with cert key this server will be able to get incoming requests and return them sanitized
#it will also reply to the connections 
class ServerObject():
  
      #Wraps a socket object to handle TLS, arguments are host address, port to access and path to SSL key files
      def __init__(self, addr, port, certpath):  

           self.req = HandleRequest
           self.sock = socket.socket()
           self.sock.bind((addr, port))
           self.sock.listen(5)
           self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
           self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
           self.context.load_cert_chain(certpath + "localhost.pem", certpath + "localhost.key")
           self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
           self.context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
           self.conn = None
           LoggingObject("INIT", "SSL server created")

      #writes a single line and sends it to the client or writes multiple lines in a loop if the reply is in a list format
      def reply(self, response):

            if(len(response[0]) <= 1):
                  self.conn.write(('HTTP/1.1 200 OK\n\n%s' % response).encode())
                    
            else:
                multi_response = ""
                for row in response:
                    multi_response += (str(row) + "\n")

                self.conn.write(('HTTP/1.1 200 OK\n\n%s' % multi_response).encode())
                  
      #this function will handle and incoming request and respond appropriately
      def handle(self, control_message):

               if(control_message != ""):
                  print("place holder for something")
                  pass
                  
               try:
                     
                   #initiallise conn when next connection is made            
                   ssock, addr = self.sock.accept()
                   self.conn = self.context.wrap_socket(ssock, server_side=True)
                   recieved = str(self.conn.recv(4096))
                   LoggingObject("REQUEST", recieved)

                   #parse arguments from connection to get list of commands and thier parameters for database operations
                   return self.req.parameterise(self.req.sanitise(recieved))  
                  
               except ssl.SSLError as e:
                   LoggingObject("ERROR", str(e))
               
               except Exception as e:
                   LoggingObject("ERROR", "handling query: " + str(e))    
              
      def close(self):
            LoggingObject("CLOSE","closing service")
            self.conn.close()
                              


                   
        
