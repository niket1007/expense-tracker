import streamlit as st
from typing import Optional

# Pages
from pages.utility import *

# MongoDb
from mongodb.mongodb import MongoDB


def init_db() -> Optional[MongoDB]:
    group_id = get_group_id(st.session_state.local_storage)
    db_obj = None
    with st.spinner("Connecting to Database", show_time=True):
        db_obj = MongoDB(db_name=group_id)
    if db_obj.check_connection_null():
        st.error("Error: {0}".format(db_obj), icon=":material/error:")
        return None
    return db_obj

@st.dialog("Add Investment")
def add_investment_record(db_obj: MongoDB, payment_options: list):
    inv_amount = st.number_input("Investment Amount", min_value=0)
    inv_type = st.text_input("Investment Type")
    inv_date = st.date_input("Date", value="today", key="inv_date")
    inv_payment_from = st.selectbox("Amount will be deducted from",
                                    payment_options,
                                    key="inv_payment_from")
    is_clicked = st.button("submit")
    
    if is_clicked:
        if (not isValidNumber(inv_amount) or 
            isEmptyString(inv_type) or 
            isEmptyString(inv_payment_from) or
            isEmptyObject(inv_date)):
            st.error("Field do not contain valid value")
        else:
            data = {
                "amount": inv_amount,
                "date": convert_date_to_str(inv_date),
                "payment_from": inv_payment_from,
                "inv_type": inv_type,
                "spent_by": get_username(st.session_state.local_storage)
            }
            status, result = db_obj.insert_investment_records(data)
            if isSuccess(status):
                st.success("Investment record added")
            else:
                st.error(result)

def update_record(db_obj: MongoDB) -> None:
    data = {
        "_id": st.session_state["_id"],
        "amount": st.session_state["inv_amount"],
        "date": convert_date_to_str(st.session_state["inv_date"]),
        "payment_from": st.session_state["inv_payment_source"],
        "inv_type": st.session_state["inv_type"]
    }
    validate_result = transaction_data_validator(data)
    if isSuccess(validate_result):
        status, result = db_obj.update_transaction_record(data)
        if not isSuccess(status):
            print("show_transaction", "update_record", result)
    else:
        print("show_transaction", "update_record", validate_result)

def delete_record(db_obj: MongoDB) -> None:
    result = db_obj.delete_transaction_record(st.session_state["_id"])
    if not isSuccess(result):
        print("show_transaction", "delete_record", result)


@st.dialog("Update-Delete Investment")
def update_delete_data(db_obj: MongoDB, key: str, data: list, payment_options: list):
    if key in st.session_state:
        row_data = data[st.session_state[key]["selection"]["rows"][0]]
        st.session_state["_id"] = row_data["_id"]

        with st.form("Update/Delete", enter_to_submit=False, border=False):
            if "Amount" in row_data:
                st.number_input("Amount", value=row_data["Amount"], key="inv_amount")

            if "Payment Source" in row_data:
                st.selectbox(
                    label="Payment Source",
                    options=payment_options,
                    index=get_index(payment_options, row_data["Payment Source"]),
                    key="inv_payment_source",
                )

            if "Date" in row_data:
                st.date_input(
                    "Date",
                    value=convert_str_to_date(row_data["Date"]),
                    key="inv_date",
                )

            if "Type" in row_data:
                st.text_input(
                    label="Investment Type",
                    value = row_data["Type"],
                    key="inv_type"
                )

            st.form_submit_button(
                "Update", type="primary", on_click=update_record, args=(db_obj,)
            )
        st.button("Delete", on_click=delete_record, args=(db_obj,))
    else:
        st.success("Action performed successfully.")

def populate_saving_data(db_obj: MongoDB, month: str, year: str, payment_options: list):
    status, total_inv_amt = db_obj.get_savings_amount(month, year)
    if isSuccess(status) and isEmptyList(total_inv_amt):
        st.error("Investment amount is zero. Please add into 'Investment' through income tab.")
        return
    elif not isSuccess(status):
        st.error(total_inv_amt)
        return

    status, inv_records = db_obj.get_investment_records(month, year)
    if not isSuccess(status):
        st.error(inv_records)
        return  
    elif isSuccess(status) and isEmptyList(inv_records):
        st.warning("No investment records found.")
        return
    
    total_inv_amt = total_inv_amt[0].get("total_amount")
    total_invested_amt = 0
    for record in inv_records:
        total_invested_amt += record["Amount"]
    st.success(f"Invested Amount/Total Investment Amount: {total_invested_amt}/{total_inv_amt}") 
    df = convert_to_df(inv_records)
    df.drop(["_id"], axis="columns", inplace=True)
    dataframe_key = "investment"
    st.dataframe(
        data=df,
        key=dataframe_key,
        column_order=[
            "Date",
            "Amount",
            "Type",
            "Payment Source",
            "Spent by",
        ],
        hide_index=True,
        selection_mode="single-row",
        on_select=lambda: update_delete_data(db_obj, dataframe_key, inv_records, payment_options))

    


def show_savings_ui(db_obj: MongoDB, payment_options: list):
    st.title("Savings Planner")
    st.warning("Create 'Investment' in payment options and category, then this page will work")

    year_list, month_list, current_month_index = get_month_and_year_list()

    col1, col2 = st.columns(2)

    with col1:
        selected_month = st.selectbox(
            "Select a month", month_list, index=current_month_index
        )

    with col2:
        selected_year = st.selectbox("Select a year", year_list)

    col3, col4 = st.columns(2)

    clicked = False
    with col3:
        clicked = st.button(
            label="Submit", key="show_transaction_button") 
    if clicked:
        populate_saving_data(db_obj, selected_month, selected_year, payment_options)

    with col4: 
        st.button("Add Investment", 
                  on_click=lambda: add_investment_record(db_obj, payment_options))

def main():
    db_obj = init_db()
    if db_obj is not None:
        payment_options = db_obj.get_payment_option_records()
        if isString(payment_options):
            st.error("Error: {0}".format(payment_options), icon=":material/error:")
            return
        elif isList(payment_options):
            payment_options = [i["pay_option_name"] for i in payment_options]
        
        show_savings_ui(db_obj, payment_options)

main()
