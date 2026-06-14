import streamlit as st
from typing import Optional

# Pages
from pages.utility import *

# MongoDB
from mongodb.mongodb import MongoDB

def init_db() -> Optional[MongoDB]:
    group_id = get_group_id(st.session_state.local_storage)
    db_obj = None
    with st.spinner("Connecting to Database", show_time=True):
        db_obj = MongoDB(db_name=group_id) 
    db_obj = MongoDB(db_name=group_id) 
    if db_obj.check_connection_null():
        st.error("Error: {0}".format(db_obj), icon=":material/error:")
        return None  
    return db_obj

def save_category(db_obj: MongoDB, category_name: str) -> None:
    if not isEmptyString(category_name):
        status, result = db_obj.insert_category_record({"name": category_name})
        if isSuccess(status):
            db_obj.clear_category_records()
            st.success("Category added successfully", icon=":material/done_all:")
        else:
            st.error("Error: {0}".format(result), icon=":material/error:")

def show_categories(categories: list) -> None:
    if isList(categories) and not isEmptyList(categories):
        with st.container(height=500, border=False):
            st.subheader("Available Categories", anchor=False)
            st.dataframe(convert_to_df(categories))
    elif isString(categories):
        st.error("Error: {0}".format(categories), icon=":material/error:")
    else:
        st.warning("No category available")

def crud_category(db_obj: MongoDB, categories: list) -> None:
    category_name = st.text_input("Enter Category Name",
                                    placeholder="Category Name",
                                    key="category_name")
    is_clicked = st.button("Save the changes")
    show_categories(db_obj, categories)
    if is_clicked:
        save_category(db_obj, category_name)
        st.rerun()
    

def main():
    db_obj = init_db()
    if db_obj is not None:    
        categories = db_obj.get_category_records()
        crud_category(db_obj, categories)

main()