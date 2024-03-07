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
from bson.json_util import dumps
import json

PORTNUM = 27017 # or 3306

userSchema = {
    "name": {'type': 'string', "required": True},
    "age": {'type': 'int', "required": True},
    "uniqueID": {'type': 'int', 'required': True},
    "medicalRecord": []
}

userRecordSchema = {  
    "category": [],
    "dateCreated": {'type': 'string', "required": True},
    "createdBy": {'type': 'string', "required": True},
    "description": {'type': 'string', "required": True}
}



class RequestHandler(BaseHTTPRequestHandler):
    
    def requestData(reqData):
        content_length = int(reqData.headers['Content-Length'])
        body = reqData.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        
        reqData.id = data.get('id')
        reqData.name = data.get('name')
        reqData.content = data.get('content')
        reqData.permissions = data.get('permission') #TODO

    dbConn = dbConnection.mongoConnection()
    
    def do_GET(getReq):
        """
            Handles Get requests to the server.
            
            *Returns all notes from database only 
            if the user has root/admin permissions
        """
        try:
            result = getReq.dbConn.users.find()
            resultList = list(result)
            isEmpty = len(list(result))
            if(not isEmpty):
                print(f"[SERVER]: {resultList}") 
                getReq.wfile.write(json.dumps({"result": "test"}).encode('utf-8'))
                getReq.send_response(200)
            else:
                print(f"[SERVER]: Query did not return any!")
                getReq.send_response(200)
            
            getReq.send_header('Content-type', 'application/json')
            getReq.end_headers()
            
        except Exception as e:
            print(f"[SERVER]: Error has occured: {e}")
    
    def do_PUT(putReq):
        try:
            putReq.requestData()

            myDict = {"name": putReq.name}
            putReq.dbConn.insert_one(myDict)
            
            putReq.send_response(200)
        except Exception as e:
            print(f"[SERVER]: Error has occured: {e}")

        putReq.send_header('Content-type', 'application/json')
        putReq.end_headers()


        
def run(serverClass=HTTPServer, handlerClass=RequestHandler, port = PORTNUM):
    serverAddress = ('localhost', port)
    httpd = HTTPServer(serverAddress, RequestHandler)
    print(f'[DEBUGGING]: Starting Server, running on Port: [{PORTNUM}]\n')
    httpd.serve_forever()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass 
    httpd.server_close()
    print('[DEBUGGING]: Server Has Stopped!')

if __name__ == '__main__':
    run()



