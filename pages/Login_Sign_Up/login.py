import streamlit as st 
from pages.utility import *
from pages.db import user_info_db

def init_db():
    conn = get_db_connection()
    db = user_info_db.UserInfoDB(conn)
    result = db.create_login_table()
    if isSuccess(result):
        result = db.create_group_user_table()
        if isSuccess(result):
            return db
    if not isSuccess(result):
        st.cache_resource.clear()
        st.error("Error: {0}".format(result))

def login_func(**data: dict) -> None:
    if isEmpty(data["username"]) or isEmpty(data["password"]):
        st.error("Please enter your username and password")
    else: 
        result = data["user_info_db"].fetch_user(data)
        #print("login result", result)
        if not isList(result):
            st.cache_resource.clear()
            st.error("Error: {0}".format(result))
            return
        st.session_state["isUserLoggedIn"] = True
        st.session_state["logged_user_info"] = result[0]
        # data["user_info_db"].close()

def main():
    """
    Login Page
    """

    # Initialize the database connection
    user_info_db = init_db()

    # Check if connection is successful
    if not isEmptyObject(user_info_db):
        st.header("Login", divider="blue")
        username = st.text_input("Enter your username", placeholder="Username", key="login_username")
        password = st.text_input("Enter your password", type="password", placeholder="Password", key="login_password")
        data = {}
        data["user_info_db"] = user_info_db
        data["username"] = username
        data["password"] = password
        st.button("Login", on_click=login_func, kwargs=(data), key="login_button")

main()
