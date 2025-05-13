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

def login_func(db_obj: object, data: dict) -> None:
    if isEmpty(data["username"]) or isEmpty(data["password"]):
        st.error("Please enter your username and password", icon=":material/error:")
    else: 
        result = user_info_db.fetch_user(db_obj, data)
        if not isList(result):
            if str(result) != "User doesn't exist.":
                user_info_db.cache_clear()
            st.error("Error: {0}".format(result), icon=":material/error:")
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
    if isMongoDbObject(db_obj):
        st.header("Login", divider="blue", anchor=False)
        username = st.text_input("Enter your username", placeholder="Username", key="login_username")
        password = st.text_input("Enter your password", type="password", placeholder="Password", key="login_password")
        data = {}
        data["username"] = username
        data["password"] = password
        st.button("Login", on_click=login_func, args=(db_obj, data), key="login_button")


main()
