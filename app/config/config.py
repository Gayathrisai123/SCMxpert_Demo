from pydantic import BaseSettings
from dotenv import load_dotenv
import os
import pymongo
from pymongo import MongoClient,mongo_client

load_dotenv(dotenv_path=".env")

class Settings:   

    #----------------- Database variables (MongoDB) --------------------------


    MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    client = pymongo.MongoClient(os.getenv("DATABASE_URL"))

    db = client["scmxpertlite"]
    user_collection = db.users
    shipment_collection = db.shipment
    streaming_collection = db.datastream

    #------------------ Token, authentication variables ---------------------

    SECRET_KEY=os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")   
    ACCESS_TOKEN_EXPIRE = 30 # in mins  
    COOKIE_NAME = os.getenv("COOKIE_NAME")

    # ---- Host parameters
    
    HOST = os.getenv("HOST")
    PORT = (os.getenv("PORT"))

    


settings = Settings()
