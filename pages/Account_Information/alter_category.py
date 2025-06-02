import streamlit as st
from pages.db import custom_db
from pages.utility import *

def init_db():
    group_id = get_group_id(st.session_state.local_storage)
    db_obj = custom_db.create_user_info_mongo_connection(group_id)
    if not isMongoDbObject(db_obj):
        custom_db.clear_cache()
        st.error("Error: {0}".format(db_obj), icon=":material/error:")
        return None
    return db_obj

def save_category(db_obj: object, category_name: str) -> None:
    if not isEmptyString(category_name):
        result = custom_db.insert_category_record(
            db_obj,{"name": category_name})
        if isSuccess(result):
            custom_db.clear_cache("Cache_Data")
            st.success("Category added successfully", icon=":material/done_all:")
        else:
            custom_db.clear_cache()
            st.error("Error: {0}".format(result), icon=":material/error:")

def show_categories(categories: list) -> None:
    if not isList(categories):
        custom_db.clear_cache()
        st.error("Error: {0}".format(categories), icon=":material/error:")    
    elif not isEmptyList(categories):
        with st.container(height=500, border=False):
            st.subheader("Available Categories", anchor=False)
            st.dataframe(convert_to_df(categories))

def crud_category(db_obj: object, categories: list) -> None:
    category_name = st.text_input("Enter Category Name",
                                    placeholder="Category Name",
                                    key="category_name")
    st.button("Save the changes",
            on_click=save_category, 
            args=(db_obj, category_name))
    show_categories(categories)

def main():
    db_obj = init_db()
    if isMongoDbObject(db_obj):    
        categories = custom_db.fetch_all_categories(db_obj)
        crud_category(db_obj, categories)

main()