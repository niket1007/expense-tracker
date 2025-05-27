import streamlit as st
from pages.db import custom_db
from pages.utility import *

def init_db() -> object | None:
    group_id = st.session_state["logged_user_info"]["group_id"]
    db_obj = custom_db.create_user_info_mongo_connection(group_id)
    if not isMongoDbObject(db_obj):
        custom_db.clear_cache()
        st.error("Error: {0}".format(db_obj), icon=":material/error:")
        return None
    return db_obj

def save_transaction(db_object: object, data: dict) -> None:
    result = custom_db.insert_transaction_record(db_object, data)
    if isSuccess(result):
        st.success("Transaction recorded.", icon=":material/done_all:")
    else:
        custom_db.clear_cache("Cache_Resource")
        st.error("Error: {0}".format(result), icon=":material/error:")

def income_tab(db_object: object, payment_options: list) -> None:
    with st.form("income_form", border=False, enter_to_submit=False, clear_on_submit=True):
        
        st.header("Income", divider="blue", anchor=False)
        
        amount = st.text_input("Enter the amount",
                               placeholder="Amount",
                               key="credit_amount") 
        
        transaction_date = st.date_input("Date",
                                        value="today",
                                        key="income_date")
        
        payment_to = st.selectbox("Amount added to",
                                  payment_options,
                                  key="credit_option")
        
        data = {
            "amount": amount,
            "type": "Income",
            "date":transaction_date.strftime("%d-%b-%Y"),
            "payment_to": payment_to,
            "spent_by": st.session_state["logged_user_info"]["username"]
        }
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            valid = transaction_data_validator(data)
            if isSuccess(valid):
                save_transaction(db_object, data)
            else:
                st.error("Error: {0}".format(valid), icon=":material/error:")

def main() -> None:
    """
    Transaction Record Page (Income)
    """
    db_object = init_db()
    if isMongoDbObject(db_object):

        payment_options = custom_db.fetch_all_payment_options(db_object)
        if not isList(payment_options):
            st.error("Error: {0}".format(payment_options), icon=":material/error:")
            custom_db.clear_cache()
            return
        else:
            payment_options = [i["pay_option_name"] for i in payment_options]     
            income_tab(db_object, payment_options)

main()
