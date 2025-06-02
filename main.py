
import streamlit as st
from streamlit_local_storage import LocalStorage

def log_out():
    st.session_state.local_storage.deleteAll()
    st.session_state.clear()
    st.cache_data.clear()
    st.cache_resource.clear()

def main():

    if "localstorage" not in st.session_state:
        st.session_state.local_storage = LocalStorage()

    isUserLoggedIn = False
    if st.session_state.local_storage.getItem("isUserLoggedIn") is not None:
        isUserLoggedIn = True

    if not isUserLoggedIn:
        pages_list = {
            "Login/Sign Up": [
                st.Page("pages/Login_Sign_Up/login.py", title="Login", icon=":material/login:"),
                st.Page("pages/Login_Sign_Up/signup.py", title="Sign Up", icon=":material/login:")
            ]
        }
    else:
        pages_list = {
            "Your Account": [
                st.Page("pages/Account_Information/user_info.py", title="User Details", icon=":material/account_circle:"),
                st.Page("pages/Account_Information/alter_category.py", url_path="category" ,title="Category", icon=":material/category:" ),
                st.Page("pages/Account_Information/alter_payment_options.py", url_path="payment_options", title="Payment Options", icon=":material/add_card:")
            ],
            "Record Transaction": [
                st.Page("pages/Record_Transaction/payment.py", url_path="payment", title="Payment", icon=":material/currency_rupee:", default=True),
                st.Page("pages/Record_Transaction/income.py", url_path="income", title="Income", icon=":material/money_bag:"),
                st.Page("pages/Record_Transaction/transfer.py", url_path="transfer", title="Transfer", icon=":material/swap_horiz:")
            ],
            "Expenditure Analysis": [
                st.Page("pages/Analysis/expenditure_analysis_main.py", url_path="expenditure_analysis", title="Expenditure Analysis", icon=":material/monitoring:"),
                st.Page("pages/Analysis/show_transaction.py", url_path="show_transactions", title="Show Transaction", icon=":material/receipt_long:")
            ]
        }
        sidebar = st.sidebar
        sidebar.button("Log Out", on_click=log_out)
    
    selected_page = st.navigation(pages_list)
    selected_page.run()

main()