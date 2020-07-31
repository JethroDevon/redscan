#!/usr/bin/env python3

import sys, socketserver, getopt, json
sys.path.append("classes/")
from serverObject import ServerObject
from loggingObject import LoggingObject
from db import DB

#inits server object which will, mainages user input  
def main():
  
  port = 0
  host = ""
  keyfile = ""
  database_url = ""
  server_control_message = ""
  
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

    db = DB(database_url); # initialising the database object with the url of the hosted csv file
    server = ServerObject(host, port, keyfile)

    while True:

        #server object could accept incoming signals - may accept a signal to shut down or point at a different db etc
        parameters = server.handle(server_control_message)
 
        if(parameters == None):
          continue

        #prepare to return a string containing the response from the database
        response = "NOT FOUND"
        
        if("authuser" in parameters and "passwordhash" in parameters):  
            response = db.usertokenRequest(parameters.get("authuser"),parameters.get("passwordhash"))
          
        #if user and token exist
        elif("username" in parameters and "token" in parameters):
          
            #if credentials allow user to use database queries
            can_access = db.checkToken(parameters.get("username"),parameters.get("token"))
         
            if(parameters.get("command") == "time_range" and can_access):
                if "start_time" in parameters and "end_time" in parameters:
                    response = db.timeRequest(parameters.get("start_time"),parameters.get("end_time"))
                         
            elif(parameters.get("command") == "request" and can_access):
                if "column" in parameters and "value" in parameters:
                    response = db.standardRequest(parameters.get("column"), parameters.get("value"))        
                
            elif(parameters.get("command") == "tableinfo" and can_access):
               response = db.tableInfo()

            elif(parameters.get("command") == "markRead" and can_access):
              print("four")
              if "id" in parameters and "status" in parameters:
                response = db.setURead(parameters.get("id"), parameters.get("status"))

        if(response != None):
            print (str(response))
            server.reply(response)
    
if __name__ == "__main__":

  main()
 
