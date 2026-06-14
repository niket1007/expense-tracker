import uuid
import streamlit as st 
from typing import Optional

# Pages
from pages.utility import *

# MongoDb
from mongodb.mongodb import MongoDB

def init_db() -> Optional[MongoDB]:
    db_name = st.secrets.get("user_info", {}).get("database_name", None)
    db_obj = None
    with st.spinner("Connecting to Database", show_time=True):
        db_obj = MongoDB(db_name=db_name)

    if db_obj.check_connection_null():
        st.error("Error: Unable to connect to db", icon=":material/error:")
        return None
    return db_obj

def sign_up_func(db_obj: MongoDB, data: dict) -> None:
    if isEmptyString(data["username"]) or isEmptyString(data["password"]):
        st.error("Please enter your username and password", icon=":material/error:")
    else: 
        if isEmptyString(data["group_id"]):
            data["group_id"] = str(uuid.uuid4())
        
        status, result = db_obj.insert_user(data)

        if isSuccess(status):
            local_storage_data = "{0}:{1}".format(result["username"], result["group_id"])
            st.session_state.local_storage.setItem("isUserLoggedIn", local_storage_data)
        else:
            st.error("Error: {0}".format(result), icon=":material/error:")

        

def main():
    """
    Login Page
    """
    # Initialize the database connection
    db_obj = init_db()

    # Check if connection is successful
    if db_obj is not None:
        st.header("Sign Up", divider="blue", anchor=False)
        username = st.text_input("Enter your username", placeholder="Username",key="signup_username")
        password = st.text_input("Enter your password", type="password", placeholder="Password", key="signup_password")
        group_id = st.text_input("Enter your group link", placeholder="Group Link", key="signup_group_id")
        data = {}
        data["username"] = username
        data["password"] = password
        data["group_id"] = group_id
        st.button("Sign Up", on_click=sign_up_func, args=(db_obj, data), key="signup_button")

main()