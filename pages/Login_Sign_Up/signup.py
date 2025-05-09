import uuid
import streamlit as st 
from pages.utility import *
from pages.db import user_info_db 


def init_db():
    db_obj = user_info_db.create_user_info_mongo_connection()
    if isEmptyObject(db_obj):
        st.cache_data.clear()
        st.error("Error: {0}".format(db_obj))
        return None
    return db_obj

def sign_up_func(db_obj: object, data: dict) -> None:
    if isEmpty(data["username"]) or isEmpty(data["password"]):
        st.error("Please enter your username and password")
    else: 
        if isEmpty(data["group_id"]):
            data["group_id"] = str(uuid.uuid4())
        
        result = user_info_db.insert_user(db_obj, data)

        if not isList(result):
            if str(result) != "User already exist.":
                st.cache_resource.clear()
            st.error("Error: {0}".format(result))
            return
        st.session_state["isUserLoggedIn"] = True
        st.session_state["logged_user_info"] = result[0]

def main():
    """
    Login Page
    """
    # Initialize the database connection
    db_obj = init_db()

    # Check if connection is successful
    if not isEmptyObject(db_obj):
        st.header("Sign Up", divider="blue")
        username = st.text_input("Enter your username", placeholder="Username",key="signup_username")
        password = st.text_input("Enter your password", type="password", placeholder="Password", key="signup_password")
        group_id = st.text_input("Enter your group link", placeholder="Group Link", key="signup_group_id")
        data = {}
        data["username"] = username
        data["password"] = password
        data["group_id"] = group_id
        st.button("Sign Up", on_click=sign_up_func, args=(db_obj, data), key="signup_button")

main()