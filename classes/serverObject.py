#!/usr/bin/env python3
import ssl, socket, sys
from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
from loggingObject import LoggingObject
from handleRequest import HandleRequest

#once initialised incoming data will be ha
class ServerObject():

      
      #Wraps a socket object to handle TLS, arguments are host address, port to access and path to SSL key files
      def __init__(self, addr, port, certpath):  

           self.req = HandleRequest
           self.sock = socket.socket()
           self.sock.bind((addr, port))
           self.sock.listen(5)
           self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
           self.context.load_cert_chain(certfile=(certpath + "cert.pem"), keyfile=(certpath + "key.pem"))
           self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
           self.context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
           LoggingObject("INIT", "SSL server created")

      def reply(self, connection, response):

            connection.write('HTTP/1.1 200 OK\n\n%s' % response.encode())
            #TO DO: check for closing a second connection here, im not sure

      #this function will handle and incoming request and respond appropriately
      def handle(self):

               #initiallise conn when next connection is made
               conn = None
               ssock, addr = self.sock.accept()
           
               try:

                   conn = self.context.wrap_socket(ssock, server_side=True)
                   recieved = str(conn.recv(4096))
                   LoggingObject("REQUEST", recieved)

                   #parse arguments from connection
                   parameters = self.req.sanitise(recieved)
                   
                   self.reply(conn, parameters)

               except ssl.SSLError as e:
                   LoggingObject("ERROR", str(e))
                   
               finally:
                   if conn:
                       conn.close()

               

        
