import sys, socketserver, getopt
sys.path.append("../lib/")
from serverObject import ServerObject

def main():
  port = 0

  try:
      opts, args = getopt.getopt(sys.argv[1:],"-p",)
      
  except getopt.GetoptError:
      print ('test.py -p <PORT>')
      sys.exit(2)
      
  for opt, arg in opts:  
    if opt == '-h':
      
       print ('restTest.py -p <PORT>')
       sys.exit()
       
    elif opt in ("-p"):
      port = int(str(args[0]))
    
       
  # Create the server, binding to localhost on port
  if(port != 0):

    server = socketserver.TCPServer(("127.0.0.1", port), ServerObject)
    server.handle_request()

if __name__ == "__main__":
  main()
