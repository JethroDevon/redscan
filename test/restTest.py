import sys, socketserver, getopt
sys.path.append("../lib/")
from serverObject import ServerObject



#test class for debugging
def main():
  
  port = 0
  host = ""
  
  try:
      opts, args = getopt.getopt(sys.argv[1:],'i:p:h',['ip=','port=','help'])
      
  except getopt.GetoptError:
      print ('incorrect input: test.py -i <HOST IP> -p <PORT> | -h for help')
      sys.exit(2)
      
  for opt, arg in opts:  
    if opt == '-h':
      
       print ('restTest.py -i <HOST IP> -p <PORT>')
       sys.exit()

    elif opt in ("-i","ip="):
      host = str(arg)

    elif opt in ("-p","port="):
      port = int(str(arg))




      
  # Create the server, binding to localhost on port
  if(port != 0 and host != ""):

    server = ServerObject(host, port, "../testKeys/")
    server.handle()
 
if __name__ == "__main__":
  main()
