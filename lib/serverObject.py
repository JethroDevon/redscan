#!/usr/bin/env python3
import ssl, socket
from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
from loggingObject import LoggingObject
#from handleRequest import HandleRequest

CRTPATH = "../testKeys/"

# This class contains the functionality for the restful server, it will also be responsible for validating incoming data
class ServerObject():

      def __init__(self, addr, port, certpath):  

           self.sock = socket.socket()
           self.sock.bind((addr, port))
           self.sock.listen(5)
           self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
           self.context.load_cert_chain(certfile=(certpath + "cert.pem"), keyfile=(certpath + "key.pem"))
           self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
           self.context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
           LoggingObject("INIT", "TLS server created", )

           
           
      def handle(self):

           # TO DO: add handling to this loop otherwise is messy
           while(True):
                 
               conn = None
               ssock, addr = self.sock.accept()
           
               try:

                   conn = self.context.wrap_socket(ssock, server_side=True)
                   LoggingObject("REQUEST",str(conn.recv(1024)))
                   conn.write(b'HTTP/1.1 200 OK\n\n%s' % "this is too hard".encode())
                   #process whatever

               except ssl.SSLError as e:
                   LoggingObject("ERROR", str(e))
                   
               finally:
                   if conn:
                       conn.close()

               

           LoggingObject("LOG", "closing connection exiting program")
