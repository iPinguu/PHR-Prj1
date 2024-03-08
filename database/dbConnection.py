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

from pymongo import MongoClient

def mongoConnection():
    """
        Establishes a connection with the mongoDB and returns a MongoClient Object
    """

    mongoHost = "localhost"
    mongoPort = 27017

    client = MongoClient(mongoHost, mongoPort)

    try:
        client.admin.command('ping')
        print("[SERVER]: Pinged your deployment. You successfully connected to MongoDB!")    
        return client
    except Exception as e:
        print(f'[SERVER]: {e}')
