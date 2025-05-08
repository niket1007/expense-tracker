import streamlit as st
from pages.db import custom_db
from pages.utility import *

def init_db():
    #print(st.session_state)
    db_name = st.session_state["logged_user_info"]["group_id"]
    conn = get_db_connection()
    db = custom_db.CustomDb(conn, db_name)
    result = db.create_tables()
    if isSuccess(result):
        return db
    if not isSuccess(result):
        st.cache_resource.clear()
        st.error("Error: {0}".format(result))

def save_category(category_name, db):
    if not isEmpty(category_name):
        result = db.insert_category_record({"category_name": category_name})
        if isSuccess(result):
            st.success("Category added successfully")
            st.cache_resource.clear()
        else:
            st.cache_resource.clear()
            st.error("Error: {0}".format(result))

def crud_category(category_dict, db):
    with st.form("crud_category", border=False, enter_to_submit=False):
        category_name = st.text_input("Enter Category Name", placeholder="Category Name", key="category_name")
        submitted = st.form_submit_button("Save the changes")
        if submitted:
            save_category(category_name, db)
            category_dict = db.fetch_category_records()
        if not isList(category_dict):
            st.cache_resource.clear()
            st.error("Error: {0}".format(category_dict))    
        elif not isEmptyList(category_dict):
            st.subheader("Available Categories")
            st.table(convert_to_df(category_dict))

def main():
    custom_db = init_db()
    if not isEmptyObject(custom_db):
        category_dict = custom_db.fetch_category_records()
        if not isList(category_dict):
            st.cache_resource.clear()
            st.error("Error: {0}".format(category_dict))
            return
        
    crud_category(category_dict, custom_db)

main()