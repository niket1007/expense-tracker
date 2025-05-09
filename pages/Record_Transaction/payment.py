import streamlit as st
from pages.utility import *
from pages.db import custom_db
from streamlit_qrcode_scanner import qrcode_scanner

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

@st.dialog("Payment Apps")
def show_payment_app_buttons():
    st.link_button("Paytm", "intent://upi#Intent;scheme=paytmmp;package=net.one97.paytm;end;")
    st.link_button("PhonePe", "intent://home#Intent;scheme=phonepe;package=com.phonepe.app;end;")
    st.link_button("Google Pay", "intent://upi#Intent;scheme=tez;package=com.google.android.apps.nbu.paisa.user;end;")
        
def save_transaction(data, db):
    result = transaction_data_validator(data)
    if isSuccess(result):
        result = db.insert_transaction_record(data)
    return result

def payment_tab(category_list, money_source_list, db):
    with st.form("payment_form", border=False, enter_to_submit=False):
        st.header("Payment", divider="red")
        amount = st.text_input("Enter the amount", placeholder="Amount", key="payment_amount") 
        transaction_date = st.date_input("Date", value="today", key="payment_date")
        category_option = st.selectbox("Select a category", category_list, key="payment_category")
        payment_from = st.selectbox("Amount will be deducted from", money_source_list, key="payment_deduct")

        data = {
            "amount": amount,
            "transaction_type": "Payment",
            "transaction_date": transaction_date.strftime("%d-%m-%Y"),
            "payment_from": payment_from,
            "payment_to": "",
            "category_name": category_option
        }
        
        submitted = st.form_submit_button("Pay (Add record)")
        if submitted:
            status = save_transaction(data, db)
            if isSuccess(status):
                show_payment_app_buttons()
                st.success("Transaction recorded.")
            else:
                st.cache_resource.clear()
                st.error("Error: {0}".format(status))

def main():
    """
    Transaction Record Page (Payment)
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
            payment_tab(category_list, money_source_list, custom_db)
        
main()
