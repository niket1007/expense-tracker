
import streamlit as st

def main():
    if "isUserLoggedIn" not in st.session_state:
        st.session_state["isUserLoggedIn"] = False
    if "logged_user_info" not in st.session_state:
        st.session_state["logged_user_info"] = {}
    
    if not st.session_state["isUserLoggedIn"]:
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
                st.Page("pages/Record_Transaction/payment.py", url_path="payment", title="Payment", icon=":material/currency_rupee:"),
                st.Page("pages/Record_Transaction/income.py", url_path="income", title="Income", icon=":material/money_bag:"),
                st.Page("pages/Record_Transaction/transfer.py", url_path="transfer", title="Transfer", icon=":material/swap_horiz:")
            ],
            "Budget": [
                st.Page("pages/Budget/create_budget.py", url_path="create_budget", title="Create Budget", icon=":material/savings:"),
                st.Page("pages/Budget/show_budget.py", url_path="show_budget", title="Show Budget", icon=":material/savings:")
            ],
            "Expenditure Analysis": [
                st.Page("pages/Analysis/expenditure_analysis.py", url_path="expenditure_analysis", title="Expenditure Analysis", icon=":material/monitoring:"),
                st.Page("pages/Analysis/show_transaction.py", url_path="show_transactions", title="Show Transaction", icon=":material/receipt_long:")
            ]
        }
    selected_page = st.navigation(pages_list)
    selected_page.run()

main()