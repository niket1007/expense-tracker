import streamlit as st
from typing import Optional

# Pages
from pages.utility import *
from pages.Analysis.per_user_spent import main as per_user_spent_main
from pages.Analysis.category_wise_spent import main as category_wise_spent_main

# MongoDb
from mongodb.mongodb import MongoDB

def init_db() -> Optional[MongoDB]:
    group_id = get_group_id(st.session_state.local_storage)
    db_obj = MongoDB(db_name=group_id)

    if db_obj.check_connection_null():
        st.error("Error: Unable to connect to db", icon=":material/error:")
        return None

    return db_obj

def expenditure_analysis(db_obj: MongoDB) -> None:
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
            per_user_spent_main(db_obj, data)

        # Show Category Expenses
        with st.expander("Category wise expenses"):
            category_wise_spent_main(db_obj, data)


def main():
    """
    Expenditure Analysis Page
    """

    db_object = init_db()
    if db_object is not None:
        expenditure_analysis(db_object)
        
main()