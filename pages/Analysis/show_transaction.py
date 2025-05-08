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

def show_transactions(db):
    st.header("Show Transaction", divider="blue")
    year_list, month_list = get_month_and_year_list()
    with st.form("show transaction", border=False, enter_to_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            selected_year = st.selectbox("Select a year", year_list)
        with col2:
            selected_month = st.selectbox("Select a month", month_list)
        submitted = st.form_submit_button("Submit")
        if submitted:
            selected_month_num = "0{}".format(str(month_list.index(selected_month)+1))
            result = db.fetch_transaction_records(selected_year,selected_month_num)
            if isList(result):
                #print(result)
                result = convert_to_df(result)
                st.table(result)
            else:
                st.cache_resource.clear()
                st.error("Error: {0}".format(result))

def main():
    custom_db = init_db()
    if not isEmptyObject(custom_db):
        show_transactions(custom_db)

main()