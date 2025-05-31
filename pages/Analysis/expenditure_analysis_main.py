import streamlit as st
from pages.utility import *
from pages.Analysis.per_user_spent import main as per_user_spent_main
from pages.Analysis.category_wise_spent import main as category_wise_spent_main
from pages.db import custom_db


def init_db() -> None:
    group_id = st.session_state["logged_user_info"]["group_id"]
    db_obj = custom_db.create_user_info_mongo_connection(group_id)
    if not isMongoDbObject(db_obj):
        custom_db.clear_cache()
        st.error("Error: {0}".format(db_obj), icon=":material/error:")
        return None
    return db_obj


def expenditure_analysis(db_obj: object) -> None:
    st.header("Expenditure Analysis", divider="blue", anchor=False)

    year, month, current_month_index = get_month_and_year_list()
    
    col1, col2 = st.columns(2)
    
    with col1:
        month = st.selectbox("Select a month", month, index=current_month_index, key="analysis_month")
    
    with col2:
        year = st.selectbox("Select a year", year, key="analysis_year")
    
    clicked = st.button("Show Analysis")
    
    if clicked:
        data = {
            "month": month,
            "year": year
        }

        # Show per user expenses
        with st.expander("User wise expenses"):
            per_user_spent_main(db_obj, custom_db, data)

        # Show Category Expenses
        with st.expander("Category wise expenses"):
            category_wise_spent_main(db_obj, custom_db, data)


def main():
    """
    Expenditure Analysis Page
    """

    db_object = init_db()
    if isMongoDbObject(db_object):
        expenditure_analysis(db_object)
        
main()