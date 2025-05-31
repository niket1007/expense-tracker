import streamlit as st
from pages.db import custom_db
from pages.utility import *

def init_db() -> object | None:
    group_id = st.session_state["logged_user_info"]["group_id"]
    db_obj = custom_db.create_user_info_mongo_connection(group_id)
    if not isMongoDbObject(db_obj):
        custom_db.clear_cache()
        st.error("Error: {0}".format(db_obj), icon=":material/error:")
        return None
    return db_obj

def transform_data() -> dict:
    print("reahced here")
    data = None
    if st.session_state["type"] == "Payment": 
        data = {
            "_id": st.session_state["_id"],
            "type": st.session_state["type"],
            "amount": st.session_state["record_amount"],
            "date": convert_date_to_str(st.session_state["record_date"]),
            "payment_from": st.session_state["record_payment_from"],
            "category": st.session_state["record_category"]
        }
    elif st.session_state["type"] == "Income":
        data = {
            "_id": st.session_state["_id"],
            "type": st.session_state["type"],
            "amount": st.session_state["record_amount"],
            "date": convert_date_to_str(st.session_state["record_date"]),
            "payment_to": st.session_state["record_payment_to"],
        }
    else:
        data = {
            "_id": st.session_state["_id"],
            "type": st.session_state["type"],
            "amount": st.session_state["record_amount"],
            "date": convert_date_to_str(st.session_state["record_date"]),
            "payment_from": st.session_state["record_payment_from"],
            "payment_to": st.session_state["record_payment_to"]
        }
    return data

def update_record(db_obj: object) -> None:
    data = transform_data()
    result = transaction_data_validator(data)
    if isSuccess(result):
        result = custom_db.update_transaction_record(db_obj, data)
        if not isSuccess(result):
            custom_db.clear_cache("Cache_Resource")
            print("show_transaction", "update_record", result)
    else:
        print("show_transaction", "update_record", result)

def delete_record(db_obj: object) -> None:
    result = custom_db.delete_transaction_record(db_obj, st.session_state["_id"])
    if not isSuccess(result):
        custom_db.clear_cache("Cache_Resource")
        print("show_transaction", "delete_record", result)

@st.dialog("Show data")
def show_data(db_obj: object, data: dict, key: str) -> None:

    if key in st.session_state:
        row_data = data[st.session_state[key]["selection"]["rows"][0]]
        st.session_state["type"] = row_data["type"]
        st.session_state["_id"] = row_data["_id"]
        
        #Update form
        with st.form("Update/Delete", enter_to_submit=False, border=False):
            if "amount" in row_data:
                st.text_input("Amount",
                              value = row_data["amount"],
                              key="record_amount")

            if "payment_from" in row_data:
                st.selectbox(label="Payment From",
                            options=payment_options,
                            index=get_index(payment_options, row_data["payment_from"]),
                            key="record_payment_from")
                
            if "payment_to" in row_data:
                st.selectbox(label="Payment To",
                            options=payment_options,
                            index=get_index(payment_options, row_data["payment_to"]),
                            key="record_payment_to")
                
            if "date" in row_data:
                st.date_input("Date",
                            value=convert_str_to_date(row_data["date"]),
                            key="record_date")
            if "category" in row_data:
                st.selectbox(label = "Select a category",
                            options=category_list,
                            index=get_index(category_list, row_data["category"]),
                            key="record_category")

            st.form_submit_button("Update",
                                              type="primary",
                                              on_click=update_record,
                                              args=(db_obj,))

        #Delete Button
        st.button("Delete", on_click=delete_record, args=(db_obj,))
    else:
        st.success("Action performed successfully.")

def populate_table(db_obj, selected_month, selected_year) -> None:
    filter = {
            "date": {
                "$regex": "{0}-{1}".format(selected_month, selected_year), 
                "$options": "i"
                }
            }
    results = custom_db.fetch_transaction_records_with_filters(db_obj, filter,{})
    if isList(results):
        if not isEmptyList(results):
            total_balance = {}
            transaction_records = {"Income": [], "Payment": [], "Transfer": []}

            for record in results:
                if record["type"] == "Income":
                    if record["payment_to"] in total_balance:
                        total_balance[record["payment_to"]] += int(record["amount"])
                    else:
                        total_balance[record["payment_to"]] = int(record["amount"])
                    
                    transaction_records["Income"].append(record)

                elif record["type"] == "Payment":
                    if record["payment_from"] in total_balance:
                        total_balance[record["payment_from"]] -= int(record["amount"])
                    else:
                        total_balance[record["payment_from"]] = -int(record["amount"])
                    
                    transaction_records["Payment"].append(record)

                elif record["type"] == "Transfer":
                    if record["payment_from"] in total_balance:
                        total_balance[record["payment_from"]] -= int(record["amount"])
                    else:
                        total_balance[record["payment_from"]] = -int(record["amount"])
                    if record["payment_to"] in total_balance:
                        total_balance[record["payment_to"]] += int(record["amount"])
                    else:
                        total_balance[record["payment_to"]] = int(record["amount"]) 
                    
                    transaction_records["Transfer"].append(record)

            with st.container(height=200, border=False):
                for payment_option in total_balance:
                    amount = total_balance[payment_option]
                    st.badge(
                        "{0}: {1}".format(payment_option, amount), 
                        color="green" if amount > 0 else "red")

            if not isEmptyList(transaction_records["Payment"]):
                with st.expander("Show all the Expense records", icon=":material/currency_rupee:"):
                    with st.container(height=300, border=False):
                        df = convert_to_df(transaction_records["Payment"])
                        df.drop(["type", "_id"], axis='columns', inplace=True)
                        st.dataframe(df,
                                    height=300,
                                    key="payment_data",
                                    on_select=lambda : show_data(db_obj,
                                                                transaction_records["Payment"],
                                                                "payment_data"))

            if not isEmptyList(transaction_records["Income"]):
                with st.expander("Show all the Income records", icon=":material/money_bag:"):
                    with st.container(height=300, border=False):
                        df = convert_to_df(transaction_records["Income"])
                        df.drop(["type", "_id"], axis='columns', inplace=True)
                        st.dataframe(df,
                                    height=300,
                                    key="income_data",
                                    on_select=lambda : show_data(db_obj,
                                                                transaction_records["Income"],
                                                                "income_data"))
            
            if not isEmptyList(transaction_records["Transfer"]):
                with st.expander("Show all the Transfer records", icon=":material/swap_horiz:"):
                    with st.container(height=300, border=False):
                        df = convert_to_df(transaction_records["Transfer"])
                        df.drop(["type", "_id"], axis='columns', inplace=True)
                        st.dataframe(df,
                                    height=300,
                                    key="transfer_data",
                                    on_select=lambda : show_data(db_obj,
                                                                transaction_records["Transfer"],
                                                                "transfer_data"))
    else:
        custom_db.clear_cache("Cache_Resource")
        st.error("Error: {0}".format(results), icon=":material/error:")

def show_transactions(db_obj):
    
    st.header("Show Transaction", divider="blue", anchor=False)
    
    year_list, month_list, current_month_index = get_month_and_year_list()
       
    col1, col2 = st.columns(2)
    
    with col1:
        selected_month = st.selectbox("Select a month", month_list, index=current_month_index)
    
    with col2:
        selected_year = st.selectbox("Select a year", year_list)

    clicked = st.button(
        label="Submit",
        key = "show_transaction_button")
    
    if clicked:
        populate_table(db_obj, selected_month, selected_year)

def main():
    db_obj = init_db()
    if isMongoDbObject(db_obj):
        global payment_options, category_list
        payment_options = custom_db.fetch_all_payment_options(db_obj)
        if not isList(payment_options):
            st.error("Error: {0}".format(payment_options), icon=":material/error:")
            custom_db.clear_cache("Both")
            return
        else:
            payment_options = [i["pay_option_name"] for i in payment_options]

        category_list = custom_db.fetch_all_categories(db_obj)
        if not isList(category_list):
            st.error("Error: {0}".format(category_list), icon=":material/error:")
            custom_db.clear_cache("Both")
            return
        else:
            category_list = [i["category_name"] for i in category_list]

        show_transactions(db_obj)

main()