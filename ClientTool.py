#!/usr/bin/python3

import socket, ssl, gi, hashlib, re

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from datetime import datetime


#time stamp with set format for various funcions
def time():
        
    return str(datetime.now().strftime("%y%m%d%H%M"))

class Client():

    def __init__(self):

        self.token = ""
        self.CSV = ""
        self.columns = ""
    
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ClientTool.glade")
        self.builder.connect_signals(self)
       
        self.username_field = self.builder.get_object('username')
        self.password_field = self.builder.get_object('password')
        self.host_field = self.builder.get_object('host_field')
        self.value_field = self.builder.get_object('value')
        
        self.column_field = self.builder.get_object('column')
        self.header_list = Gtk.ListStore(str)
        self.cell = Gtk.CellRendererText()
        self.column_box = self.builder.get_object('column_box')
        self.column_box.pack_start(self.cell, True)
        self.column_box.set_model(model=self.header_list)
        self.column_box.connect("changed",self.on_column_combo_changed)

        self.renderer_text = Gtk.CellRendererText()
        self.window = self.builder.get_object("window1")
        self.window.set_default_size(700, 200)
        self.window.show_all()

        
    def handle(self, command):

        self.host = self.host_field.get_text()            
        self.port = int(self.host[self.host.find(':')+1:])
        self.host = self.host[:self.host.find(':')]
            
        context = ssl.create_default_context()
        sock = socket.socket(socket.AF_INET)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_verify_locations('testKeys/localhost.pem')
        conn = context.wrap_socket(sock, server_hostname=self.host)       
        conn.connect((self.host, self.port))
        
        try:

            output = "POST /" + command + " HTTP/1.1\n"
            conn.write(output.encode())
            return conn.recv().decode()
            
        except Exception as e:
            print("error:" + str(e))

        finally:
            conn.close()

        return "failed to recieve from server - maybe re-authenticate or check network connections"

    
    def query(self, button):
     
        if(self.token != "" and self.host != "" and self.port != 0):

            req = self.buildQueryString(self.column_field.get_text(), self.value_field.get_text())
            self.CSV = self.handle(req)
            print(self.CSV)

    #creates an sql query that gets rows where cols have (value)
    def buildQueryString(self, cols, value):

          self.host = self.host_field.get_text()   #get this working then make it a function
          self.port = int(self.host[self.host.find(':')+1:])   
          return "username=" + self.username_field.get_text() + "&token=" + self.token + "&command=request&column=" + cols + "&value=" + value

    #creates string for requesting token with user
    def buildAuthRequestString(self):
       return "authuser=" + self.username_field.get_text()  + "&passwordhash=" + self.createPasswordHash(self.password_field.get_text())

             
    def requestHeaders(self):
     
        if(self.token != "" and self.username_field.get_text() != ""):
            return self.handle("username=" + self.username_field.get_text() + "&token=" + self.token + "&command=tableinfo")
       

    def getToken(self, button):
        
            self.token = self.handle(self.buildAuthRequestString())
            self.token = self.token[-64:]
            self.populateColumnBox(self.requestHeaders())
        

    def populateColumnBox(self, server_response):

        for line in server_response.split("\n"):
            name_start = line.find("'")
            if(name_start != -1):

                part_one_str = line[name_start+1:]           
                self.header_list.append([part_one_str[:part_one_str.find("'")]])

        self.column_box.add_attribute(self.cell, "text",0)
        self.column_box.set_active(0)
        
    def on_column_combo_changed(self, combo):
        
        act = combo.get_active()
        if act is not None:
            self.column_field.set_text(self.header_list[act][0])

            
    def createPasswordHash(self, password):

        pwdhashobj = hashlib.sha256(("CAKE" + password + "CAKE").encode('utf_8'))
        hashvalue = time() + pwdhashobj.hexdigest()
        outhashobj = hashlib.sha256(hashvalue.encode('utf_8'))
        return outhashobj.hexdigest()

    
    def onDestroy(self, *args):
        Gtk.main_quit()

#run client app!
if __name__ == "__main__":
      
  main = Client()
  Gtk.main()
