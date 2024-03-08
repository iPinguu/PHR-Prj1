## Project Description
BTP405 - Project 1
Professor Maziar Sojoudian

## Author
Franz Luiz Sy
116322223

## Purpose Summary
A place for users to store, edit, and retrieve health related information 

## Target Features
Security - user authentication and permissions <br />
Scalability - data storage can accommodate increasing data size <br />
Maintainable - simple code implementation to keep maintenance simple and easy <br />
Accessibility - user friendly, user centered <br />
Cloud based - wider user reach, both consumer and developer. Containerized for maximum compatibility, benefiting maintainability.

## Repository Guide
- [Prerequisites](#prerequisites)
- [API Documentation](#API-Documentation)
- [Dependencies](#dependencies)

## Prerequisuites 
Must Have the following installed

- Python
- MongoDB
- Docker

then clone the repo 
`git clone https://github.com/iPinguu/PHR-Prj1.git`
`cd PHR-Prj1 `

cd into database folder, then run this command on the CLI
`docker-compose up -d`

this will run the monggodb server


## Dependencies
- Pip
- Pymongo

## API-Documentation
  def do_GET(getReq):
        """
            Handles find_one() Get requests to the server.
            
            Returns a single document from the database
            and only the user's documents

            TODO: Security and Permissions Logic (users cannot access other's file if theyre not authorized by the record owner)
        """
 
 def do_PUT(putReq):
        """
            Insert, override if it already exists

            Used to update a user's credentials
        """

def do_POST(postReq):
        """
            Inserts a new document in the database

            used when a user signs up for an account

 def do_DELETE(deleteREQ):
        """
            Deletes a document in the database

            Used when user wants to delete their account

            TODO: confirmation Logic (ask user if theyre REALLY REALLY SURE)
        """