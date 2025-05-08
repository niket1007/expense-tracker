import pandas as pd
from datetime import date
import json
import streamlit as st
import sqlitecloud as sqllite


# ------------------------------Cache Function Start

@st.cache_resource
def get_db_connection():
    """ create a database connection to a SQLite database """
    try:
        #print("called in utility.py")
        conn = sqllite.connect(st.secrets["sqllite"]["db_url"])
        return conn
    except sqllite.Error as e:
        # #print(f"Error connecting to database: {e}")
        st.cache_resource.clear()
        return e

@st.cache_resource
def get_payment_options(_db):
    return _db.fetch_payment_option_records()

@st.cache_resource
def get_category(_db):
    return _db.fetch_category_records()

# ------------------------------Cache Function End


# ------------------------------Utility Function Start
def isEmpty(value:str) -> bool:
    """
    Check if a string is empty or contains only whitespace characters.
    """
    if type(value) == str:
        return value is None or value.strip() == ""
    raise TypeError("Value must be a string")

def isEmptyObject(value:object) -> bool:
    """
    Check if a database object is empty or None.
    """
    return value is None

def isEmptyList(value:list) -> bool:
    """
    Check if a list is empty.
    """
    return value is None or len(value) == 0

def isEmptyDict(value:dict) -> bool:    
    """
    Check if a dictionary is empty.
    """
    return value is None or len(value) == 0

def isDict(value:object) -> bool:
    """
    Check if a value is a dictionary.
    """
    return isinstance(value, dict)
def isList(value:object) -> bool:   
    """
    Check if a value is a list.
    """
    return isinstance(value, list)

def isSuccess(result:object) -> bool:
    """
    Check if the result is a success message.
    """
    return result == "Success"

def convert_to_df(data: dict) -> object:
    """
    Convert a dict to a DataFrame.
    """
    return pd.DataFrame(data)

def transaction_data_validator(data: dict):
    valid = "Success"
    if data["transaction_type"] == "Income":
        for key in data:
            if key != "payment_from" and isEmpty(data[key]):
                valid = "Provide value for {0}".format(key)
                return valid
    elif data["transaction_type"] == "Payment":
        for key in data:
            #print(key, type(data[key]))
            if key != "payment_to" and isEmpty(data[key]):
                valid = "Provide value for {0}".format(key)
                return valid

    elif data["transaction_type"] == "Transfer":
        for key in data:
            if key != "category_name" and isEmpty(data[key]):
                valid = "Provide value for {0}".format(key)
                return valid        
        if data["payment_from"] == data["payment_to"]:
            valid = "Transfer from and to option cannot be same."
            return valid
    return valid

def get_month_and_year_list(current=False):
    current_year = int(date.today().strftime("%Y"))
    current_month = date.today().strftime("%b")
    year = [str(year) for year in range(current_year, current_year+10)]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July"
            , "Aug", "Sept", "Oct", "Nov", "Dec"]
    
    return [year, month]

def convert_to_json(data):
    """
    Convert stringified json to dictionary
    """
    if not isEmpty(data):
        return json.loads(data)

# ------------------------------Utility Function End