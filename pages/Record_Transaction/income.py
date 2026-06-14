import streamlit as st
from typing import Optional

# Pages
from pages.utility import *

# MongoDb
from mongodb.mongodb import MongoDB

def init_db() -> Optional[MongoDB]:
    group_id = get_group_id(st.session_state.local_storage)
    db_obj = MongoDB(db_name=group_id)

    if db_obj.check_connection_null():
        st.error("Error: Unable to connect to db", icon=":material/error:")
        return None

    return db_obj

def income_tab(db_obj: MongoDB, payment_options: list) -> None:
    with st.form("income_form", border=False, enter_to_submit=False, clear_on_submit=True):
        
        st.header("Income", divider="blue", anchor=False)
        
        amount = st.number_input("Enter the amount",
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
            "date": convert_date_to_str(transaction_date),
            "payment_to": payment_to,
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
        if isList(payment_options):
            payment_options = [i["pay_option_name"] for i in payment_options]     
            income_tab(db_obj, payment_options)
        elif isString(payment_options):
            st.error("Error: {0}".format(payment_options), icon=":material/error:")
            return

main()
