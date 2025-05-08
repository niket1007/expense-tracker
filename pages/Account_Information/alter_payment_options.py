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

def save_payment_option(payment_source_name, db):
    if not isEmpty(payment_source_name):
        result = db.insert_money_source_record({"payment_option_name": payment_source_name})
        if isSuccess(result):
            st.success("Payment option added successfully")
            st.cache_resource.clear()
        else:
            st.cache_resource.clear()
            st.error("Error: {0}".format(result))

def crud_payment_options(money_source_dict, db):
    with st.form("crud_payment", border=False, enter_to_submit=False):
        payment_source_name = st.text_input("Enter Payment option name", placeholder="Payment Option Name", key="payment_option_name")
        submitted = st.form_submit_button("Save the changes")
        if submitted:
            save_payment_option(payment_source_name, db)
            money_source_dict = db.fetch_payment_option_records()
        if not isList(money_source_dict):
            st.cache_resource.clear()
            st.error("Error: {0}".format(money_source_dict))    
        elif not isEmptyList(money_source_dict):
            st.subheader("Available Payment options")
            st.table(convert_to_df(money_source_dict))

def main():
    custom_db = init_db()
    if not isEmptyObject(custom_db):
        money_source_dict = custom_db.fetch_payment_option_records()
        if not isList(money_source_dict):
            st.cache_resource.clear()
            st.error("Error: {0}".format(money_source_dict))
            return

    crud_payment_options(money_source_dict, custom_db)

main()