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
from bson import json_util
import json

PORTNUM = 8080 # or 3306

class UserSchemas:
    def __init__(self, name=None, age=None, unique_id=None, medical_record=None, canBeEditedByAuthorizedUsers=None):
        self.name = name
        self.age = age
        self.unique_id = unique_id
        self.medical_record = medical_record or [],
        canBeEditedByAuthorizedUsers = canBeEditedByAuthorizedUsers or False

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "uniqueID": self.unique_id,
            "medicalRecord": self.medical_record,
            "canBeEditedByAuthorizedUsers": self.editByAuthorizedUsers
        }

class userRecord:
    def __init__(self,category=None, date_created=None, created_by=None, description=None):
        self.category = category or []
        self.date_created = date_created
        self.created_by = created_by
        self.description = description
        
    def to_dict(self):
        return {
            "category": self.category,
            "dateCreated": self.date_created,
            "createdBy": self.created_by,
            "description": self.description
        }


class RequestHandler(BaseHTTPRequestHandler):
    
    def requestData(reqData):
        content_length = int(reqData.headers['Content-Length'])
        body = reqData.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        
        reqData.id = data.get('id')
        reqData.age = data.get('age')
        reqData.name = data.get('name')
        reqData.medicalRecord = data.get('medicalRecord')
        reqData.permissions = data.get('permission')

    dbConn = dbConnection.mongoConnection()
    userCollection = dbConn['PHR']['users']
    
    def do_GET(getReq):
        """
            Handles find_one() Get requests to the server.
            
            Returns a single document from the database
            and only the user's documents

            TODO: Security and Permissions Logic (users cannot access other's file if theyre not authorized by the record owner)
        """
        try:
            dbQuery = getReq.userCollection.find_one()
            isEmpty = len(list(dbQuery))
            response = {"result": json.loads(json_util.dumps(dict(dbQuery)))}
            
            if(not isEmpty):
                print(f"[SERVER]: Query did not return any!")
                response = {"result": json.loads(json_util.dumps("[SERVER]: Query did not return any!"))}
                getReq.send_response(404)
            else:
                print(f"[SERVER]: {dict(dbQuery)}")
                getReq.send_response(200)
                  
            getReq.send_header('Content-type', 'application/json')
            getReq.end_headers()
            getReq.wfile.write(json.dumps(response).encode('utf-8'))                
            
        except Exception as e:
            print(f"[ERROR]: Error has occured: {e}")
    
    def do_PUT(putReq):
        """
            Insert, override if it already exists

            Used to update a user's credentials
        """
        putReq.requestData()
        
        try:
            # if putReq.path == '/session/profile/edit':
                    if(not len(putReq.name) and not len(putReq.age)):
                        putReq.userCollection.find_one_and_update(
                        {'uniqueID': putReq.id}, 
                        {'$set': {'name': putReq.name, 'age': putReq.age}})
                    
                    if(not len(putReq.name)):
                        putReq.userCollection.find_one_and_update(
                        {'uniqueID': putReq.id}, 
                        {'$set': {'name': putReq.name}})
                    
                    if(not len(putReq.age)):
                         putReq.userCollection.find_one_and_update(
                        {'uniqueID': putReq.id}, 
                        {'$set': {'age': putReq.age}})
            
            # if putReq.path == '/session/userNum/editMedicalRecord':
                # if(not len(putReq.medicalRecord)):
                #     if(putReq.userCollection.find({"authorizedEditors": {"$exists": True, "$eq": putReq.id}})):
                #         putReq.userCollection.find_one_and_update(
                #             {'uniqueID':putReq.id},
                #             {'$set': {'medicalRecords': userRecordSchema}}
                #         )
        
        except Exception as e:
            print(f"[ERROR]: Error has occured: {e}")
    
    def do_POST(postReq):
        """
            Inserts a new document in the database

            used when a user signs up for an account
        """
        postReq.requestData()

        try:
            if((postReq.userCollection.find_one({'uniqueID': postReq.id})) is None):
                
                newUser = UserSchemas(
                    name=postReq.name,
                    age=postReq.age,
                    unique_id=postReq.id,
                    medical_record=[],
                    canBeEditedByAuthorizedUsers=postReq.permissions
                )        
                
                postReq.userCollection.insert_one({newUser})

                postReq.send_response(200) 
                response = {"result": json.loads(json_util.dumps("[SERVER] User Added Successfully"))}
            else:
                postReq.send_response(409) 
                response = {"result": json.loads(json_util.dumps("[SERVER] User Already Exists!"))}

        except Exception as e:
            print(f"[ERROR]: Error has occured: {e}")

        postReq.send_header('Content-type', 'application/json')
        postReq.end_headers()
        postReq.wfile.write(json.dumps(response).encode('utf-8'))

    def do_DELETE(deleteREQ):
        """
            Deletes a document in the database

            Used when user wants to delete their account

            TODO: confirmation Logic (ask user if theyre REALLY REALLY SURE)
        """

        deleteREQ.requestData()

        try:
            if((deleteREQ.userCollection.find_one({'uniqueID': int(deleteREQ.id)})) is None):
                deleteREQ.send_response(404) 
                response = {"result": json.loads(json_util.dumps("[SERVER] User Doesnt Exists!"))}
            else:
                deleteREQ.userCollection.delete_one({'uniqueID': int(deleteREQ.id),'name': deleteREQ.name})
                deleteREQ.send_response(200) 
                response = {"result": json.loads(json_util.dumps("[SERVER] User Deleted Successfully"))}

        except Exception as e:
            print(f"[ERROR]: Error has occured: {e}")

        postReq.send_header('Content-type', 'application/json')
        postReq.end_headers()
        postReq.wfile.write(json.dumps(response).encode('utf-8'))

        
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



