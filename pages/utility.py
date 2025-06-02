import pandas as pd
from datetime import date, datetime
import pymongo


# ------------------------------Utility Function Start
def isEmptyString(value:str) -> bool:
    """
    Check if a string is empty or contains only whitespace characters.
    """
    return value is None or value.strip() == ""
    

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

def convert_to_df(data: dict | list, columns: list = None) -> object:
    """
    Convert a dict to a DataFrame.
    """
    if not isEmptyList(columns):
        return pd.DataFrame(data.items(), columns=columns)
    return pd.DataFrame(data)
    

def transaction_data_validator(data: dict):
    valid = "Success"

    for key in data:
        if key == "_id":
            if data[key] is None:
                valid = "Provide value for {0}".format(key)
                return valid  
        elif key == "amount":
            continue
        elif isEmptyString(data[key]):
            valid = "Provide value for {0}".format(key)
            return valid 
    
    if data["type"] == "Transfer" and data["payment_from"] == data["payment_to"]:
        valid = "Transfer from and to payment option cannot be same"
        return valid

    return valid

def get_month_and_year_list():
    current_year = int(date.today().strftime("%Y"))
    current_month = date.today().strftime("%b")
    year = [str(year) for year in range(current_year, current_year+10)]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"
            , "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    return [year, month, month.index(current_month)]

def convert_date_to_str(data):
    return date.strftime(data, "%d-%b-%Y")

def convert_str_to_date(data):
    return datetime.strptime(data, "%d-%b-%Y")

def get_index(elements, find_element):
    try:
        return elements.index(find_element)
    except ValueError as e:
        return None

# ------------------------------Utility Function End