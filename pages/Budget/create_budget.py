import streamlit as st
from pages.db import custom_db
from pages.utility import *

def init_db() -> None:
    group_id = st.session_state["logged_user_info"]["group_id"]
    db_obj = custom_db.create_user_info_mongo_connection(group_id)
    if not isMongoDbObject(db_obj):
        custom_db.clear_cache()
        st.error("Error: {0}".format(db_obj), icon=":material/error:")
        return None
    return db_obj

def create_budget(db_object: object) -> None:
    """
    Create budget for a particular year and month
    """

    st.header("Create Budget", divider="blue", anchor=False)
    
    with st.form("create_budget"):
        
        year, month, current_month_index = get_month_and_year_list()
        
        col1, col2 = st.columns(2)
        
        with col1:
            month = st.selectbox("Select month", month, index=current_month_index)
        
        with col2:
            year = st.selectbox("Select year", year)
        
        category_list = custom_db.fetch_all_categories(db_object)
        
        if isList(category_list):
            
            if not isEmptyList(category_list):
                
                for category in category_list:
                    category["budget"] = 0
                
                changed_df = st.dataframe(convert_to_df(category_list), on_select="ignore")
                
                submitted = st.form_submit_button("Create")
                
                if submitted:
                
                    data = {
                        "year": year,
                        "month": month,
                        "budget": changed_df.to_json(orient='records')
                    }
                    result = custom_db.insert_budget_record(db_object, data)
                    
                    if isSuccess(result):
                        st.success("Budget Added", icon=":material/done_all:")
                    else:
                        custom_db.clear_cache()
                        st.error("Error: {0}".format(result), icon=":material/error:")
        else:
            custom_db.clear_cache()
            st.error("Error: {0}".format(category_list), icon=":material/error:")


def main() -> None:
    db_object = init_db()
    if isMongoDbObject(db_object):
        create_budget(db_object)

main()
