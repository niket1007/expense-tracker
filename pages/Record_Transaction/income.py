import streamlit as st
from pages.utility import *
from pages.db import custom_db

def init_db():
    db_name = st.session_state["logged_user_info"]["group_id"]
    conn = get_db_connection()
    db = custom_db.CustomDb(conn, db_name)
    result = db.create_tables()
    if isSuccess(result):
        return db
    if not isSuccess(result):
        st.cache_resource.clear()
        st.error("Error: {0}".format(result))

def save_transaction(data, db):
    result = db.insert_transaction_record(data)
    if isSuccess(result):
        st.success("Transaction recorded.")
    else:
        st.cache_resource.clear()
        st.error("Error: {0}".format(result))

def income_tab(category_list, money_source_list, db):
    with st.form("income_form", border=False, enter_to_submit=False):
        st.header("Income", divider="blue")
        amount = st.text_input("Enter the amount", placeholder="Amount", key="credit_amount") 
        transaction_date = st.date_input("Date", value="today", key="income_date")
        category_option = st.selectbox("Select a category", category_list, key="credit_category")
        payment_to = st.selectbox("Amount added to", money_source_list, key="credit_option")
        
        data = {
            "amount": amount,
            "transaction_type": "Income",
            "transaction_date":transaction_date.strftime("%d-%m-%Y"),
            "payment_from": "",
            "payment_to": payment_to,
            "category_name": category_option
        }
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            valid = transaction_data_validator(data)
            if isSuccess(valid):
                save_transaction(data, db)
            else:
                st.error(valid)

def main():
    """
    Transaction Record Page (Income)
    """
    custom_db = init_db()
    if not isEmptyObject(custom_db):
        
        money_source_list = get_payment_options(custom_db)
        if not isList(money_source_list):
            st.error("Error: {0}".format(money_source_list))
            st.cache_resource.clear()
            return
        else:
            money_source_list = [i["payment_option_name"] for i in money_source_list]

        category_list = get_category(custom_db)
        if not isList(category_list):
            st.error("Error: {0}".format(category_list))
            st.cache_resource.clear()
            return
        else:
            category_list = [i["category_name"] for i in category_list]        
            income_tab(category_list, money_source_list, custom_db)

main()
