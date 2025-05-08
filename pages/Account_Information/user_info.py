import streamlit as st

def logout_func() -> None:
    st.session_state["isUserLoggedIn"] = False
    st.session_state["logged_user_info"] = {}
    st.session_state.clear()

def main():
    """
    User Information Page
    """
    #print(st.session_state)
    st.title("Welcome {0}".format(st.session_state["logged_user_info"]["username"]))

    st.markdown("Group Id: **{0}**".format(st.session_state["logged_user_info"]["group_id"]))
    st.markdown(":blue[This is your group id. Share this with your friends to add them to your group.]")
    st.button("Logout", on_click=logout_func, key="logout_button")

main()
