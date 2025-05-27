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

def populate_table(db_obj, selected_month, selected_year) -> None:
    filter = {
            "date": {
                "$regex": "{0}-{1}".format(selected_month, selected_year), 
                "$options": "i"
                }
            }
    results = custom_db.fetch_transaction_records_with_filters(db_obj, filter)
    if isList(results):
        if not isEmptyList(results):
            total_balance = {}
            transaction_records = {"Income": [], "Payment": [], "Transfer": []}

            for record in results:
                if record["type"] == "Income":
                    if record["payment_to"] in total_balance:
                        total_balance[record["payment_to"]] += int(record["amount"])
                    else:
                        total_balance[record["payment_to"]] = int(record["amount"])
                    
                    transaction_records["Income"].append(record)

                elif record["type"] == "Payment":
                    if record["payment_from"] in total_balance:
                        total_balance[record["payment_from"]] -= int(record["amount"])
                    else:
                        total_balance[record["payment_from"]] = -int(record["amount"])
                    
                    transaction_records["Payment"].append(record)

                elif record["type"] == "Transfer":
                    if record["payment_from"] in total_balance:
                        total_balance[record["payment_from"]] -= int(record["amount"])
                    else:
                        total_balance[record["payment_from"]] = -int(record["amount"])
                    if record["payment_to"] in total_balance:
                        total_balance[record["payment_to"]] += int(record["amount"])
                    else:
                        total_balance[record["payment_to"]] = int(record["amount"]) 
                    
                    transaction_records["Transfer"].append(record)

            with st.container(height=200, border=False):
                for payment_option in total_balance:
                    amount = total_balance[payment_option]
                    st.badge(
                        "{0}: {1}".format(payment_option, amount), 
                        color="green" if amount > 0 else "red")

            if not isEmptyList(transaction_records["Payment"]):
                with st.expander("Show all the Expense records", icon=":material/currency_rupee:"):
                    with st.container(height=300, border=False):
                        st.table(transaction_records["Payment"])

            if not isEmptyList(transaction_records["Income"]):
                with st.expander("Show all the Income records", icon=":material/money_bag:"):
                    with st.container(height=300, border=False):
                        st.table(transaction_records["Income"])
            
            if not isEmptyList(transaction_records["Transfer"]):
                with st.expander("Show all the Transfer records", icon=":material/swap_horiz:"):
                    with st.container(height=300, border=False):
                        st.table(transaction_records["Transfer"])
    else:
        custom_db.clear_cache("Cache_Resource")
        st.error("Error: {0}".format(results), icon=":material/error:")

def show_transactions(db_obj):
    
    st.header("Show Transaction", divider="blue", anchor=False)
    
    year_list, month_list, current_month_index = get_month_and_year_list()
       
    col1, col2 = st.columns(2)
    
    with col1:
        selected_month = st.selectbox("Select a month", month_list, index=current_month_index)
    
    with col2:
        selected_year = st.selectbox("Select a year", year_list)

    clicked = st.button(
        label="Submit",
        key = "show_transaction_button")
    
    if clicked:
        populate_table(db_obj, selected_month, selected_year)

def main():
    db_obj = init_db()
    if isMongoDbObject(db_obj):
        show_transactions(db_obj)

main()