import streamlit as st

# Pages
from pages.utility import *

# MongoDb
from mongodb.mongodb import MongoDB


def show_group_users() -> None:
    group_id = get_group_id(st.session_state.local_storage)
    db_name = st.secrets.get("user_info", {}).get("database_name")
    db_obj = None
    with st.spinner("Connecting to Database", show_time=True):
        db_obj = MongoDB(db_name=db_name) 
    if db_obj.check_connection_null():
        st.error("Error: Unable to connect to db", icon=":material/error:")
        return None
    
    result = db_obj.get_users_group(group_id)
    if isList(result):
        st.table(result)
    else:
        st.error("Error: {0}".format(result), icon=":material/error:")   

def main() -> None:
    """
    User Information Page
    """
    st.title("Welcome {0}".format(get_username(st.session_state.local_storage)))

    st.markdown("Group Id: **{0}**".format(get_group_id(st.session_state.local_storage)))
    st.markdown(":blue[This is your group id. Share this with your friends to add them to your group.]")
    
    show_group_users()

main()
