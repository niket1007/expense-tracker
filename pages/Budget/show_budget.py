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


def show_budget(db):
    """
    Show budget for a particular month
    """
    with st.form("show_budget"):
        year, month = get_month_and_year_list()
        col1, col2 = st.columns(2)
        with col1:
            month = st.selectbox("Select month", month)
        with col2:
            year = st.selectbox("Select year", year)
        submitted = st.form_submit_button("Show Budget")
        if submitted:
            result = db.fetch_budget_record({"year": year, "month": month})
            if not isList(result):
                st.cache_resource.clear()
                st.error(result)
            else:
                if not isEmptyList(result):
                    budget_json = convert_to_json(result[0]["budget"])
                    st.table(budget_json)

def main():
    custom_db = init_db()
    if not isEmptyObject(custom_db):
        st.header("Budget", divider="blue")
        show_budget(custom_db)
        
main()
