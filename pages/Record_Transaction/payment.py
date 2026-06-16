import streamlit as st
from typing import Optional

# Pages
from pages.utility import *

# MongoDb
from mongodb.mongodb import MongoDB

def init_db() -> Optional[MongoDB]:
    group_id = get_group_id(st.session_state.local_storage)
    db_obj = None
    with st.spinner("Connecting to Database", show_time=True):
        db_obj = MongoDB(db_name=group_id)

    if db_obj.check_connection_null():
        st.error("Error: Unable to connect to db", icon=":material/error:")
        return None

    return db_obj

@st.dialog("Payment Apps")
def show_payment_app_buttons() -> None:
    st.link_button("Paytm", "intent://upi#Intent;scheme=paytmmp;package=net.one97.paytm;end;")
    st.link_button("PhonePe", "intent://home#Intent;scheme=phonepe;package=com.phonepe.app;end;")
    st.link_button("Google Pay", "intent://upi#Intent;scheme=tez;package=com.google.android.apps.nbu.paisa.user;end;")


def payment_tab(db_obj: MongoDB, category_list: list, payment_options: list) -> None:
    with st.form("payment_form", border=False, enter_to_submit=False, clear_on_submit=True):
        
        st.header("Payment", divider="red", anchor=False)
        
        amount = st.number_input("Enter the amount",
                               placeholder="Amount",
                               key="payment_amount") 
        
        transaction_date = st.date_input("Date",
                                         value="today",
                                         key="payment_date")
        
        category_option = st.selectbox("Select a category",
                                       category_list,
                                       key="payment_category")
        payment_from = st.selectbox("Amount will be deducted from",
                                    payment_options,
                                    key="payment_deduct")

        data = {
            "amount": amount,
            "type": "Payment",
            "date": convert_date_to_str(transaction_date),
            "payment_from": payment_from,
            "category": category_option,
            "spent_by": get_username(st.session_state.local_storage)
        }
        
        submitted = st.form_submit_button("Pay (Add record)")
        if submitted:
            validate_result = transaction_data_validator(data)
            if isSuccess(validate_result):
                status, result = db_obj.insert_transaction_record(data)
                if isSuccess(status):
                    show_payment_app_buttons()
                    st.success("Transaction recorded.", icon=":material/done_all:")
                else:
                    st.error("Error: {0}".format(result), icon=":material/error:")
            else:
                st.error("Error: {0}".format(validate_result), icon=":material/error:")

def main() -> None:
    """
    Transaction Record Page (Payment)
    """
    db_obj = init_db()
    if db_obj is not None:
        payment_options = db_obj.get_payment_option_records()
        if isString(payment_options):
            st.error("Error: {0}".format(payment_options), icon=":material/error:")
            return
        elif isList(payment_options):
            payment_options = [i["pay_option_name"] for i in payment_options]


        category_list = db_obj.get_category_records()
        if isString(category_list):
            st.error("Error: {0}".format(category_list), icon=":material/error:")
            return 
        elif isList(category_list):
            category_list = [i["category_name"] for i in category_list]
        
        payment_tab(db_obj, category_list, payment_options)
        
main()
