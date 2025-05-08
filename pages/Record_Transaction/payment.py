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

# def payment_app__link_button():
#     st.link_button("Paytm", "paytmmp://pay?pa=your@vpa&pn=YourName&tn=Note&am=1&cu=INR")
#     st.link_button("PhonePe", "phonepe://pay?pa=your@vpa&pn=YourName&tn=Note&am=1&cu=INR")
#     st.link_button("Google Pay", "tez://upi/pay?pa=your@vpa&pn=YourName&tn=Note&am=1&cu=INR")

@st.dialog("QR Scanner")
def open_camera(data: dict, db: object):
    scanned_qr_code = qrcode_scanner(key='qrcode_scanner')

    if scanned_qr_code:
        print(data, scanned_qr_code)
        if not isEmpty(data["amount"]):
            scanned_qr_code += "&am=" + data["amount"]
        if not isEmpty(data["category_name"]):
            scanned_qr_code += "&tn=" + data["category_name"]
        paytm_link = scanned_qr_code.replace("upi", "paytmmp")
        phonepe_link = scanned_qr_code.replace("upi", "phonepe")
        gpay_link = scanned_qr_code.replace("upi://","tez://upi/")
        # print(paytm_link, gpay_link, phonepe_link)
        # st.link_button("Pay", scanned_qr_code)
        st.link_button("Paytm", paytm_link)
        st.link_button("PhonePe", phonepe_link)
        st.link_button("Google Pay", gpay_link)
        
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
        col1, col2 = st.columns(2, gap="small")
        with col1:
            submitted = st.form_submit_button("Pay(QR Scan)")
            if submitted:
                status = save_transaction(data, db)
                if isSuccess(status):
                    st.success("Transaction recorded.")
                    open_camera(data, db)
                else:
                    st.cache_resource.clear()
                    st.error("Error: {0}".format(status))
        with col2:
            submitted = st.form_submit_button("Pay (Add record)")
            if submitted:
                status = save_transaction(data, db)
                if isSuccess(status):
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
