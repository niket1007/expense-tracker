import configparser
import os
import streamlit as st
import pymongo

CONFIG_PATH = os.path.abspath('pages/db/config.ini')

def cache_clear():
    st.cache_resource.clear()

def _get_config(key1: str, key2: str) -> str:
    """Get the value of a key from the config file."""
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config.get(key1, key2)

@st.cache_resource
def create_user_info_mongo_connection() -> object:
    """ Create a database connection to a MongoDB database """
    try:
        connection_string = ""
        if "mongodb" in st.secrets and "connection_string" in st.secrets["mongodb"]:
            connection_string = st.secrets["mongodb"]["connection_string"]
        else:
            print(os.environ)
            connection_string = os.environ["mongo_db_connection_string"]
        client = pymongo.MongoClient(connection_string)
        db = client[_get_config('user_info', 'database_name')]        
        return db
    except Exception as e:
        return e

def insert_user(db: object, data: dict) -> list | str:
    """
    Insert a new user into the login table and group table
    """
    try:
        login_collection = db[_get_config('user_info', 'login_collection')]
        group_collection = db[_get_config('user_info', 'group_user_collection')]        
        
        # Check if the username already exists
        if login_collection.find_one({"username": data["username"]}):
            raise Exception("User already exist.")

        # Insert user into login table
        login_collection.insert_one({
            "username": data["username"],
            "password": data["password"]
        })

        # Insert user into group table
        group_collection.insert_one({
            "group_id": data["group_id"],
            "username": data["username"]
        })

        return [{
            "username": data["username"],
            "group_id": data["group_id"]
        }]
    except Exception as e:
        return e

def fetch_user(db: object, data: dict) -> dict | str:
    """ 
    Insert a new user into the login table and group table 
    """
    try:
        login_collection = db[_get_config("user_info", "login_collection")]
        group_collection = db[_get_config("user_info", "group_user_collection")]

        # Fetch record from login collection
        result_login = login_collection.find_one({
            "username": data["username"], 
            "password": data["password"]})
        
        if result_login:
            #Fetch record from group_user collection on basis of username
            result_group = group_collection.find_one({
                "username": data["username"]})
        else:
            raise Exception("User doesn't exist.")

        return [{
            "username": result_login["username"],
            "group_id": result_group["group_id"]
        }]
    except Exception as e:
        return e

def fetch_group_users(db: object, group_id: str) -> list | str:
    """
    Fetch all users from group_user table on basis of group_id
    """
    try:
        group_collection = db[_get_config("user_info", "group_user_collection")]

        #Fetch records from group_user collection on basis of group_id
        result_group = group_collection.find({
                    "group_id": group_id})

        return [
            {"username": group["username"]} for group in result_group
        ]
    except Exception as e:
        return e
