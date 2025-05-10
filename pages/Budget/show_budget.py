import streamlit as st
from pages.db import custom_db
from pages.utility import *

def init_db() -> None:
    group_id = st.session_state["logged_user_info"]["group_id"]
    db_obj = custom_db.create_user_info_mongo_connection(group_id)
    if not isMongoDbObject(db_obj):
        custom_db.clear_cache()
        st.error("Error: {0}".format(db_obj))
        return None
    return db_obj

def show_budget(db_object: object) -> None:
    """
    Show budget for a particular month
    """
    
    year, month = get_month_and_year_list()
    
    col1, col2 = st.columns(2)
    
    with col1:
        month = st.selectbox("Select month", month)
    
    with col2:
        year = st.selectbox("Select year", year)
    
    clicked = st.button("Show Budget")
    
    if clicked:
        
        result = custom_db.fetch_budget_record(
            db_object,
            {"year": year, "month": month})
        
        if not isList(result):
            st.cache_resource.clear()
            st.error(result)
        else:
            if not isEmptyList(result):
                with st.container(height=500, border=False):
                    json_df = convert_to_json(result[0]["budget"])
                    st.table(json_df)

def main():
    db_object = init_db()
    if isMongoDbObject(db_object):
        st.header("Budget", divider="blue")
        show_budget(db_object)
        
main()
