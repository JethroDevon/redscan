#!/usr/bin/env python3
import sys, socketserver, getopt
sys.path.append("classes/")
from serverObject import ServerObject
from db import DB

#inits server, main loop with handled user input 
def main():
  
  port = 0
  host = ""
  keyfile = ""
  database_url = ""

  #  handle user input
  try:
      opts, args = getopt.getopt(sys.argv[1:],'i:p:k:d:h',['ip=','port=','keyfile=','database=','help'])
      
      for opt, arg in opts:  
        if opt == '-h':
      
          print ('restTest.py -i <HOST IP> -p <PORT> -k <CERT/KEY PATH> -d <database url>')
          sys.exit()

        elif opt in ("-i","ip="):
          host = str(arg)

        elif opt in ("-p","port="):
          port = int(str(arg))

        elif opt in ("-k","keyfile="):
          keyfile = str(arg)

        elif opt in ("-d","database="):
          database_url = str(arg)

  except getopt.GetoptError:
       print ('incorrect input: test.py -i <HOST IP> -p <PORT> -k <CERT/KEY PATH> -d <database url>| -h for help')
       sys.exit(2)
      
  # Create the server, binding to localhost on port
  if(port != 0 and host != ""):

    db = DB(database_url);
    server = ServerObject(host, port, keyfile)
    server.handle()
    
if __name__ == "__main__":
  main()
