import uuid
import streamlit as st 
from pages.utility import *
from pages.db import user_info_db 


def init_db():
    db_obj = user_info_db.create_user_info_mongo_connection()
    if not isMongoDbObject(db_obj):
        user_info_db.cache_clear()
        st.error("Error: {0}".format(db_obj), icon=":material/error:")
        return None
    return db_obj

def sign_up_func(db_obj: object, data: dict) -> None:
    if isEmptyString(data["username"]) or isEmptyString(data["password"]):
        st.error("Please enter your username and password", icon=":material/error:")
    else: 
        if isEmptyString(data["group_id"]):
            data["group_id"] = str(uuid.uuid4())
        
        result = user_info_db.insert_user(db_obj, data)

        if not isList(result):
            if str(result) != "User already exist.":
                user_info_db.cache_clear()
            st.error("Error: {0}".format(result), icon=":material/error:")
            return

        local_storage_data = "{0}:{1}".format(result[0]["username"], result[0]["group_id"])
        st.session_state.local_storage.setItem("isUserLoggedIn", local_storage_data)

def main():
    """
    Login Page
    """
    # Initialize the database connection
    db_obj = init_db()

    # Check if connection is successful
    if isMongoDbObject(db_obj):
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