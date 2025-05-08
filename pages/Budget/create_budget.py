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

def create_budget(db):
    """
    Create budget for a particular year and month
    """
    with st.form("create_budget"):
        year, month = get_month_and_year_list()
        col1, col2 = st.columns(2)
        with col1:
            month = st.selectbox("Select month", month)
        with col2:
            year = st.selectbox("Select year", year)
        category_list = get_category(db)
        
        for category in category_list:
            category["budget"] = 0
        changed_df = st.data_editor(convert_to_df(category_list))
        # #print(changed_df)
        submitted = st.form_submit_button("Create")
        if submitted:
            # #print(changed_df)
            data = {
                "year": year,
                "month": month,
                "budget": changed_df.to_json(orient='records')
            }
            #print(data)
            result = db.insert_budget_record(data)
            if isSuccess(result):
                st.success("Budget Added")
            else:
                st.cache_resource.clear()
                st.error("Error: {0}".format(result))


def main():
    custom_db = init_db()
    if not isEmptyObject(custom_db):
        st.header("Create Budget", divider="blue")
        create_budget(custom_db)

main()
