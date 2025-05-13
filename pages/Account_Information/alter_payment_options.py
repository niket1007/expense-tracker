import streamlit as st
from pages.db import custom_db
from pages.utility import *

def init_db():
    group_id = st.session_state["logged_user_info"]["group_id"]
    db_obj = custom_db.create_user_info_mongo_connection(group_id)
    if not isMongoDbObject(db_obj):
        custom_db.clear_cache()
        st.error("Error: {0}".format(db_obj), icon=":material/error:")
        return None
    return db_obj

def save_payment_options(db_obj: object, payment_option_name: str) -> None:
    if not isEmpty(payment_option_name):
        result = custom_db.insert_payment_option_record(
            db_obj,{"name": payment_option_name})
        if isSuccess(result):
            custom_db.clear_cache("Cache_Data")
            st.success("Payment option added successfully", icon=":material/done_all:")
        else:
            custom_db.clear_cache()
            st.error("Error: {0}".format(result), icon=":material/error:")

def show_payment_options(payment_options: list) -> None:
    if not isList(payment_options):
        custom_db.clear_cache()
        st.error("Error: {0}".format(payment_options), icon=":material/error:")    
    elif not isEmptyList(payment_options):
        with st.container(height=500, border=False):
            st.subheader("Available payment_options", anchor=False)
            st.table(convert_to_df(payment_options))

def crud_payment_options(db_obj: object, payment_options: list) -> None:
    payment_option_name = st.text_input(
        "Enter Payment option name",
        placeholder="Payment Option Name",
        key="payment_option_name")
    st.button("Save the changes",
            on_click=save_payment_options, 
            args=(db_obj, payment_option_name))
    show_payment_options(payment_options)

def main():
    db_obj = init_db()
    if isMongoDbObject(db_obj):    
        payment_options = custom_db.fetch_all_payment_options(db_obj)
        crud_payment_options(db_obj, payment_options)

main()