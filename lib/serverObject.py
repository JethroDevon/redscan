import SocketServer
from loggingObject import LoggingObject

#This class contains the functionality for the restful server, it will also be responsible for validating incoming data

class ServerObject(SocketServer.BaseRequestHandler):
 

    def handle(self):
        
        # self.request is the TCP socket connected to the client
        self.rawdata = self.request.recv(1024).strip()
        LoggingObject.("log",self.client_address[0] + " " + self.rawdata)

        # just send back the same data, but upper-cased
        self.request.sendall(self.rawdata.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
