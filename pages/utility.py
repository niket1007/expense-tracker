import pandas as pd
from datetime import date
import json
import pymongo


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

def isMongoDbObject(value: object):
    """
    Check if a value is mongo db object
    """
    return isinstance(value, pymongo.synchronous.database.Database)

def convert_to_df(data: dict) -> object:
    """
    Convert a dict to a DataFrame.
    """
    return pd.DataFrame(data)

def transaction_data_validator(data: dict):
    valid = "Success"

    # Type Validation
    if data["type"] == "Income":
        for key in data:
            if key != "payment_from" and isEmpty(data[key]):
                valid = "Provide value for {0}".format(key)
                return valid
    elif data["type"] == "Payment":
        for key in data:
            if key != "payment_to" and isEmpty(data[key]):
                valid = "Provide value for {0}".format(key)
                return valid

    elif data["type"] == "Transfer":
        for key in data:
            if key != "category" and isEmpty(data[key]):
                valid = "Provide value for {0}".format(key)
                return valid        
        if data["payment_from"] == data["payment_to"]:
            valid = "Transfer from and to option cannot be same."
            return valid

    # Field Validation
    if not data["amount"].isnumeric():
        valid = "Amount field can have only numeric values."
        return valid

    return valid

def get_month_and_year_list():
    current_year = int(date.today().strftime("%Y"))
    year = [str(year) for year in range(current_year, current_year+10)]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"
            , "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    return [year, month]

def convert_to_json(data):
    """
    Convert stringified json to dictionary
    """
    if not isEmpty(data):
        return json.loads(data)

# ------------------------------Utility Function End