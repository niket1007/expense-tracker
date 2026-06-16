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

def transfer_tab(db_obj: MongoDB, payment_options: list) -> None:
    with st.form("transfer_form", border=False, enter_to_submit=False, clear_on_submit=True):
        
        st.header("Transfer", divider="orange", anchor=False)
        
        amount = st.number_input("Enter the amount",
                               placeholder="Amount", 
                               key="transfer_amount") 
        
        transaction_date = st.date_input("Date", 
                                        value="today",
                                        key="transfer_date")
        
        transfer_from = st.selectbox("Select a transfer from",
                                    payment_options,
                                    key="transfer_from")
        
        transfer_to = st.selectbox("Select a transfer to",
                                   payment_options,
                                   key="transfer_to")   
        
        data = {
            "amount": amount,
            "type": "Transfer",
            "date": convert_date_to_str(transaction_date),
            "payment_from": transfer_from,
            "payment_to": transfer_to,
            "spent_by": get_username(st.session_state.local_storage)
        }

        submitted = st.form_submit_button("Submit")
        if submitted:
            validate_result = transaction_data_validator(data)
            if isSuccess(validate_result):
                status, result = db_obj.insert_transaction_record(data)
                if isSuccess(status):
                    st.success("Transaction recorded.", icon=":material/done_all:")
                else:
                    st.error("Error: {0}".format(result), icon=":material/error:")
            else:
                st.error("Error: {0}".format(validate_result), icon=":material/error:")

def main() -> None:
    db_obj = init_db()
    if db_obj is not None:
        payment_options = db_obj.get_payment_option_records()
        if isString(payment_options):
            st.error("Error: {0}".format(payment_options), icon=":material/error:")
            return
        elif isList(payment_options):
            payment_options = [i["pay_option_name"] for i in payment_options]
        
        transfer_tab(db_obj, payment_options)
        
main()
