import pymongo
import streamlit as st
from typing import Any, Optional

class MongoDB:
    _mongodb_instances: dict[str, Any] = {}

    def __new__(cls, db_name: str="default"):
        if db_name not in cls._mongodb_instances:
            cls._mongodb_instances[db_name] = super().__new__(cls)
        return cls._mongodb_instances[db_name]

    def __init__(self, db_name: str="default"):
        if getattr(self, "_initialised", False):
            return
        self._initialised = True
        self.connection_string: Optional[str] = st.secrets.get("mongodb", {}).get("connection_string", None)
        self._db_name: str = db_name
        self._payment_option_records: Optional[list[dict[str, str]]] = None
        self._category_records: Optional[list[dict[str, str]]] = None
        if getattr(self, "_client", None) is None or getattr(self, "_db", None) is None:
            self._client, self._db = self.initiate_connection()
    
    def reconnect_db(self):
        self._client, self._db = self.initiate_connection()

    def initiate_connection(self) -> tuple:
        try:
            if self.connection_string:
                client = pymongo.MongoClient(self.connection_string, connect=True)
                db = client.get_database(self._db_name)
                return client, db
            else:
                return None, None
        except Exception as e:
            print("Error", e)
            if getattr(self, "_client", None):
                self._client.close()
            return None, None
        
    @classmethod
    def close_connections(cls):
        for instance in cls._mongodb_instances.values():
            if getattr(instance, "_client", None):
                instance._client.close()
        cls._mongodb_instances.clear()
    
    def check_connection_null(self) -> bool:
        return self._client is None and self._db is None

    def get_payment_option_records(self) -> Optional[list[dict[str, str]]] | str:
        try:
            if self._payment_option_records is None: 
                collection_name = st.secrets.get("custom_db_info", {}).get("payment_option_collection", None)
                
                # Fetch all payment options records from collection
                results = self._db[collection_name].find()
                if results is not None:
                    self._payment_option_records = [
                        {"pay_option_name": result["name"]} for result in results]
            return self._payment_option_records
        except Exception as e:
            self.clear_payment_record_option_records()
            return str(e)
    
    def get_category_records(self) -> Optional[list[dict[str, str]]] | str:
        try:
            if self._category_records is None:
                collection_name = st.secrets.get("custom_db_info", {}).get("category_collection", None)
                
                # Fetch all category records from collection
                results = self._db[collection_name].find()
                if results is not None:
                    self._category_records = [
                        {"category_name": result["name"]} for result in results]
            return self._category_records
        except Exception as e:
            self.clear_category_records()
            return str(e)

    def get_users_group(self, group_id: str) -> list | str:
        try:
            collection_name = st.secrets.get("user_info", {}).get("group_user_collection", None)
            if collection_name:
                # Fetch records from group_user collection on basis of group_id
                result_group = self._db[collection_name].find({"group_id": group_id})
                return [
                    {"username": group["username"]} for group in result_group
                ]
            else:
                return "Unexpected error"
        except Exception as e:
            return str(e)


    def get_user(self, data: dict) -> tuple[str, str|dict]:
        try:
            login_collection_name = st.secrets.get("user_info", {}).get("login_collection", None)
            group_collection_name = st.secrets.get("user_info", {}).get("group_user_collection", None)

            if login_collection_name and group_collection_name:
                # Fetch record from login collection
                result_login = self._db[login_collection_name].find_one({
                    "username": data["username"], 
                    "password": data["password"]})
                
                if result_login:
                    #Fetch record from group_user collection on basis of username
                    result_group = self._db[group_collection_name].find_one({
                        "username": data["username"]})
                else:
                    return "Error", "User doesn't exist."

                return "Success", {
                    "username": result_login["username"],
                    "group_id": result_group["group_id"]
                }
            else:
                return "Error", "Unexpected error"
        except Exception as e:
            return "Error", str(e)
    
    def fetch_transaction_records_with_filters(
            self, pipeline: list, ) -> tuple:
        try:
            collection_name = st.secrets.get("custom_db_info", {}).get("transaction_collection", None)
            
            if collection_name: 

                # Fetch all transaction records from collection
                results = self._db[collection_name].aggregate(pipeline)

                if results is None:
                    return "Error", "No data found"
                return "Success", list(results)
            else:
                return "Error", "Unexpected error"
        except Exception as e:
            return "Error", str(e)

    def insert_user(self, data: dict) -> tuple[str, str|dict]:
        try:
            login_collection_name = st.secrets.get("user_info", {}).get("login_collection", None)
            group_collection_name = st.secrets.get("user_info", {}).get("group_user_collection", None)

            if login_collection_name and group_collection_name:
                # Check if the username already exists
                if self._db[login_collection_name].find_one({"username": data["username"]}):
                    raise Exception("User already exist.")

                # Insert user into login table
                self._db[login_collection_name].insert_one({
                    "username": data["username"],
                    "password": data["password"]
                })

                # Insert user into group table
                self._db[group_collection_name].insert_one({
                    "group_id": data["group_id"],
                    "username": data["username"]
                })

                return "Success", {
                    "username": data["username"],
                    "group_id": data["group_id"]
                }
            else:
                return "Error", "Unexpected error"
        except Exception as e:
            return "Error", str(e)


    def insert_payment_option_record(self, data: dict) -> tuple[str, str]:
        try:
            collection_name = st.secrets.get("custom_db_info", {}).get("payment_option_collection", None)
            if collection_name:
                # Update if existing record otherwise create a new one
                filter = {"name": data["name"]}
                value = {"$set": data}
                result = self._db[collection_name].update_one(filter, value, upsert=True)
                return "Success", result
            else:
                return "Error", "Unexpected error"
        except Exception as e:
            return "Error", str(e)

    def insert_category_record(self, data: dict) -> tuple[str, str]:
        try:
            collection_name = st.secrets.get("custom_db_info", {}).get("category_collection", None)
            if collection_name:
                # Update if existing record otherwise create a new one
                filter = {"name": data["name"]}
                value = {"$set": data}
                result = self._db[collection_name].update_one(filter, value, upsert=True)
                return "Success", result
            else:
                return "Error", "Unexpected error"
        except Exception as e:
            return "Error", str(e)
    
    def insert_transaction_record(self, data: dict) -> tuple:
        try:
            collection_name = st.secrets.get("custom_db_info", {}).get("transaction_collection", None)
            if collection_name:
                # Insert a new transaction record
                self._db[collection_name].insert_one(data)
                return "Success", None
            else: 
                return "Error", "Unexpected error"
        except Exception as e:
            return "Error", str(e)
    
    def update_transaction_record(self, data: dict) -> tuple:
        try:
            collection_name = st.secrets.get("custom_db_info", {}).get("transaction_collection", None)

            if collection_name:
                # Update existing record
                filter = {"_id": data["_id"]}
                value = {"$set": data}
                self._db[collection_name].update_one(filter, value, True)
                return "Success", None
            else:
                return "Error", "Unexpected error"
        except Exception as e:
            return "Error", str(e)
    
    def delete_transaction_record(self, id: object) -> str:
        try:
            collection_name = st.secrets.get("custom_db_info", {}).get("transaction_collection", None)

            if collection_name:
                # Update existing record
                query = {"_id": id}
                self._db[collection_name].delete_one(query)
                return "Success"
            else:
                return "Unexpected error"
        except Exception as e:
            return str(e)

    def clear_payment_record_option_records(self) -> None:
        self._payment_option_records = None
    
    def clear_category_records(self) -> None:
        self._category_records = None