import streamlit as st
from typing import Optional

# Pages
from pages.utility import *

# Mongodb
from mongodb.mongodb import MongoDB

def init_db() -> Optional[MongoDB]:
    group_id = get_group_id(st.session_state.local_storage)
    db_obj = None
    with st.spinner("Connecting to Database", show_time=True):
        db_obj = MongoDB(db_name=group_id) 
    if db_obj.check_connection_null():
        st.error("Error: {0}".format(db_obj), icon=":material/error:")
        return None
    return db_obj

def save_payment_options(db_obj: MongoDB, payment_option_name: str) -> None:
    if not isEmptyString(payment_option_name):
        status, result = db_obj.insert_payment_option_record({"name": payment_option_name})
        
        if isSuccess(status):
            db_obj.clear_payment_record_option_records()
            st.success("Payment option added successfully", icon=":material/done_all:")
        else:
            st.error("Error: {0}".format(result), icon=":material/error:")

def show_payment_options(payment_options: list|str) -> None:
    if isList(payment_options) and not isEmptyList(payment_options):
        with st.container(height=500, border=False):
            st.subheader("Available payment_options", anchor=False)
            st.table(convert_to_df(payment_options))
    elif isString(payment_options):
        st.error("Error: {0}".format(payment_options), icon=":material/error:")
    else:
        st.warning("No payment options available")     

def crud_payment_options(db_obj: MongoDB, payment_options: list) -> None:
    payment_option_name = st.text_input(
        "Enter Payment option name",
        placeholder="Payment Option Name",
        key="payment_option_name")
    is_clicked = st.button("Save the changes")
    show_payment_options(db_obj, payment_options)

    if is_clicked:
        save_payment_options(db_obj, payment_option_name)
        st.rerun()
        
def main():
    db_obj = init_db()
    if db_obj is not None: 
        payment_options = db_obj.get_payment_option_records() 
        crud_payment_options(db_obj, payment_options)

main()