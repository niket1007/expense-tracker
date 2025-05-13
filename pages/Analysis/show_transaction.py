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
            total = [0, 0]
            for record in results:
                if record["type"] == "Income":
                    total[0] += int(record["amount"])
                elif record["type"] == "Payment":
                    total[1] += int(record["amount"])
            with st.container(height=500, border=False):
                st.badge("Income: {0}".format(total[0]), color="green")
                st.badge("Expenses: {0}".format(total[1]), color="red")
                st.table(results)
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