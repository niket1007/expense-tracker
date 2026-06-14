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
        st.error("Error: {0}".format(db_obj), icon=":material/error:")
        return None
    return db_obj


def populate_saving_data(db_obj: MongoDB, month: str, year: str):
    pipeline = [
        {
            "$match": {
                "date": {
                    "$regex": "{0}-{1}".format(month, year),
                    "$options": "i",
                },
                "type": "Income",
                "payment_to": "Savings"
            }
        },
        {
            "$group": {
                "_id": "$category",
                "amount": {
                    "$sum": "$amount"
                }
            }
        },
        {
            "$project": {
                "_id": "type"
            }
        }
    ]
    status, result = db_obj.get_savings_amount(pipeline)


def show_savings_ui(db_obj: MongoDB):
    st.title("Savings Planner")
    st.warning("Create 'Savings' in payment options, then this page will work")

    year_list, month_list, current_month_index = get_month_and_year_list()

    col1, col2 = st.columns(2)

    with col1:
        selected_month = st.selectbox(
            "Select a month", month_list, index=current_month_index
        )

    with col2:
        selected_year = st.selectbox("Select a year", year_list)

    clicked = st.button(label="Submit", key="show_transaction_button")

    if clicked:
        populate_saving_data(db_obj, selected_month, selected_year)


def main():
    db_obj = init_db()
    if db_obj is not None:
        show_savings_ui(db_obj)


main()
