 # ****************************************************************************
 #                        	Project - #1
 # Full Name: Franz Luiz Sy
 # Student ID#: 116322223
 # Email: fsy1@myseneca.ca
 # Section: NBB
 # Date Of Completion: 03/07/2024

 # Authenticity Declaration:

 # I declare that this submittion is the reslt of my own work and has not been
 # shared to any other student or any 3rd party content distributer/provider.
 # This submitted piece of work is entirely of my creation.

 # ****************************************************************************

from database import dbConnection
from http.server import HTTPServer, BaseHTTPRequestHandler
import io as BytesIO
import json

class RequestHandler(BaseHTTPRequestHandler):
    
    def requestData(reqData):
        content_length = int(reqData.headers['Content-Length'])
        body = reqData.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        
        reqData.id = data.get('id')
        reqData.name = data.get('title')
        reqData.content = data.get('content')
        reqData.permissions = data.get('permission') #TODO
    
    def do_GET(getReq):
        """
            Handles Get requests to the server.
            
            *Returns all notes from database only 
            if the user has root/admin permissions
        """

        
         





def run(serverClass=HTTPServer, handlerClass=RequestHandler, port = PortNum):
    serverAddress = ('', port)
    httpd = HTTPServer(serverAddress, RequestHandler)
    print(f'[DEBUGGING]: Starting Server, running on Port: [{PortNum}]\n')
    httpd.serve_forever()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass 
    httpd.server_close()
    print('[DEBUGGING]: Server Has Stopped!')

if __name__ == '__main__':
    run()



