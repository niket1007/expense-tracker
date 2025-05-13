import configparser
import os
import streamlit as st
import pymongo

CONFIG_PATH = os.path.abspath('pages/db/config.ini')

def _get_config(key1: str, key2: str) -> str:
    """Get the value of a key from the config file."""
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config.get(key1, key2)

def clear_cache(option: str = "Both") -> None:
    if option == "Both":
        st.cache_data.clear()
        st.cache_resource.clear()
    elif option == "Cache_Data":
        st.cache_data.clear()
    elif option == "Cache_Resource":
        st.cache_resource.clear()
     
@st.cache_resource
def create_user_info_mongo_connection(db_name: str) -> object:
    """
    Create a database connection to a MongoDB database 
    """
    try:
        connection_string = ""
        if "mongodb" in st.secrets and "connection_string" in st.secrets["mongodb"]:
            connection_string = st.secrets["mongodb"]["connection_string"]
        else:
            connection_string = os.environ["mongo_db_connection_string"]
        client = pymongo.MongoClient(connection_string)
        db = client[db_name]        
        return db
    except Exception as e:
        return e

def insert_transaction_record(db: object, data: dict) -> str:
        """
        Insert a transaction record 
        """
        try:
            transaction_collection = db[_get_config("custom_db_info", "transaction_collection")]

            # Insert a new transaction record
            transaction_collection.insert_one(data)

            return "Success"
        except Exception as e:
            return e

def insert_category_record(db: object, data: dict) -> str:
        """ 
        Insert a category record 
        """
        try:
            category_collection = db[_get_config("custom_db_info", "category_collection")]

            # Update if existing record otherwise create a new one
            filter = {"name": data["name"]}
            value = {"$set": data}
            category_collection.update_one(filter, value, True)
                        
            return "Success"
        except Exception as e:
            return e

def insert_payment_option_record(db: object, data: dict) -> str:
        """ 
        Insert a payment option record 
        """
        try:
            payment_option_collection = db[_get_config("custom_db_info", "payment_option_collection")]
            
            # Update if existing record otherwise create a new one
            filter = {"name": data["name"]}
            value = {"$set": data}
            payment_option_collection.update_one(filter, value, True)

            return "Success"
        except Exception as e:
            return e

def insert_budget_record(db: object, data: dict) -> str:
    """
    Insert budget record
    """
    try:
        budget_collection = db[_get_config("custom_db_info", "budget_collection")]

        # Update if existing record otherwise create a new one
        filter = {"year": data["year"], "month": data["month"]}
        value = {"$set": data}
        budget_collection.update_one(filter, value, True)

        return "Success"
    except Exception as e:
        return e

def fetch_all_transaction_record(db: object) -> list|str:
    """
    Fetch all transaction records
    """
    try:
        transaction_collection = db[_get_config("custom_db_info", "transaction_collection")]

        # Fetch all transaction records from collection
        results = transaction_collection.find()

        return [] if results is None else [result for result in results]
    except Exception as e:
        return e

@st.cache_data
def fetch_all_categories(_db: object) -> list|str:
    """
    Fetch all the categories
    """
    try:
        category_collection = _db[_get_config("custom_db_info", "category_collection")]

        # Fetch all category records from collection
        results = category_collection.find()

        return [] if results is None else [{"category_name": result["name"]} for result in results]
    except Exception as e:
        return e

@st.cache_data
def fetch_all_payment_options(_db: object) -> list|str:
    """
    Fetch all transaction records
    """
    try:
        payment_option_collection = _db[_get_config("custom_db_info", "payment_option_collection")]

        # Fetch all payment options records from collection
        results = payment_option_collection.find()

        return [] if results is None else [{"pay_option_name": result["name"]} for result in results]
    except Exception as e:
        return e

def fetch_transaction_records_with_filters(db: object, filters: dict) -> list|str:
    """
    Fetch transaction records on basis of filters
    """
    try:
        transaction_collection = db[_get_config("custom_db_info", "transaction_collection")]
        
        # Fetch all transaction records from collection
        results = transaction_collection.find(
            filters,
            {"_id": 0})

        return [] if results is None else [result for result in results]
    except Exception as e:
        return e

def fetch_budget_record(db: object, filters: dict) -> list|str:
    """
    Fetch transaction records on basis of filters
    """
    try:
        budget_collection = db[_get_config("custom_db_info", "budget_collection")]
        
        # Fetch all transaction records from collection
        results = budget_collection.find_one(
            filters,
            {"_id": 0})

        return [] if results is None else [results]
    except Exception as e:
        return e
