import streamlit as st
from pages.db import user_info_db
from pages.utility import *

def logout_func() -> None:
    st.session_state.clear()
    st.cache_data.clear()
    st.cache_resource.clear()

def show_group_users() -> None:
    group_id = get_group_id(st.session_state.local_storage)
    db_obj = user_info_db.create_user_info_mongo_connection()
    if isMongoDbObject(db_obj):
        result = user_info_db.fetch_group_users(db_obj, group_id)
        if isList(result):
            st.table(result)
        else:
            user_info_db.cache_clear()
            st.error("Error: {0}".format(result), icon=":material/error:")
    else:
        user_info_db.cache_clear()
        st.error("Error: {0}".format(db_obj), icon=":material/error:")

def main() -> None:
    """
    User Information Page
    """
    st.title("Welcome {0}".format(get_username(st.session_state.local_storage)))

    st.markdown("Group Id: **{0}**".format(get_group_id(st.session_state.local_storage)))
    st.markdown(":blue[This is your group id. Share this with your friends to add them to your group.]")
    show_group_users()
    st.button("Logout", on_click=logout_func, key="logout_button")

main()
