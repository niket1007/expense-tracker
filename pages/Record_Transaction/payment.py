import streamlit as st
from pages.db import custom_db
from pages.utility import *

def init_db() -> object | None:
    # group_id = get_group_id(st.session_state.local_storage)
    group_id = get_group_id(st.session_state.local_storage)
    db_obj = custom_db.create_user_info_mongo_connection(group_id)
    if not isMongoDbObject(db_obj):
        custom_db.clear_cache()
        st.error("Error: {0}".format(db_obj), icon=":material/error:")
        return None
    return db_obj

@st.dialog("Payment Apps")
def show_payment_app_buttons() -> None:
    st.link_button("Paytm", "intent://upi#Intent;scheme=paytmmp;package=net.one97.paytm;end;")
    st.link_button("PhonePe", "intent://home#Intent;scheme=phonepe;package=com.phonepe.app;end;")
    st.link_button("Google Pay", "intent://upi#Intent;scheme=tez;package=com.google.android.apps.nbu.paisa.user;end;")
        
def save_transaction(db_obj: object, data: dict) -> None:
    result = custom_db.insert_transaction_record(db_obj, data)
    return result

def payment_tab(db_obj: object, category_list: list, payment_options: list) -> None:
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
            status = transaction_data_validator(data)
            if isSuccess(status):
                status = save_transaction(db_obj, data)
                if isSuccess(status):
                    show_payment_app_buttons()
                    st.success("Transaction recorded.", icon=":material/done_all:")
                else:
                    custom_db.clear_cache("Cache_Resource")
                    st.error("Error: {0}".format(status), icon=":material/error:")
            else:
                st.error("Error: {0}".format(status), icon=":material/error:")

def main() -> None:
    """
    Transaction Record Page (Payment)
    """
    db_obj = init_db()
    if isMongoDbObject(db_obj):
        payment_options = custom_db.fetch_all_payment_options(db_obj)
        if not isList(payment_options):
            st.error("Error: {0}".format(payment_options), icon=":material/error:")
            st.cache_resource.clear()
            return
        else:
            payment_options = [i["pay_option_name"] for i in payment_options]

        category_list = custom_db.fetch_all_categories(db_obj)
        if not isList(category_list):
            st.error("Error: {0}".format(category_list), icon=":material/error:")
            st.cache_resource.clear()
            return
        else:
            category_list = [i["category_name"] for i in category_list]    
            payment_tab(db_obj, category_list, payment_options)
        
main()
