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
        st.error("Error: Unable to connect to db", icon=":material/error:")
        return None

    return db_obj


def transform_data() -> dict:
    data = None
    if st.session_state["type"] == "Payment":
        data = {
            "_id": st.session_state["_id"],
            "type": st.session_state["type"],
            "amount": st.session_state["record_amount"],
            "date": convert_date_to_str(st.session_state["record_date"]),
            "payment_from": st.session_state["record_payment_from"],
            "category": st.session_state["record_category"],
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
            "payment_to": st.session_state["record_payment_to"],
        }
    return data


def update_record(db_obj: MongoDB) -> None:
    data = transform_data()
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


@st.dialog("Show data")
def show_data(
    db_obj: MongoDB, data: dict, key: str, payment_options: list, category_list: list
) -> None:

    if key in st.session_state:
        row_data = data[st.session_state[key]["selection"]["rows"][0]]
        st.session_state["type"] = row_data["type"]
        st.session_state["_id"] = row_data["_id"]

        # Update form
        with st.form("Update/Delete", enter_to_submit=False, border=False):
            if "amount" in row_data:
                st.number_input("Amount", value=row_data["amount"], key="record_amount")

            if "payment_from" in row_data:
                st.selectbox(
                    label="Payment From",
                    options=payment_options,
                    index=get_index(payment_options, row_data["payment_from"]),
                    key="record_payment_from",
                )

            if "payment_to" in row_data:
                st.selectbox(
                    label="Payment To",
                    options=payment_options,
                    index=get_index(payment_options, row_data["payment_to"]),
                    key="record_payment_to",
                )

            if "date" in row_data:
                st.date_input(
                    "Date",
                    value=convert_str_to_date(row_data["date"]),
                    key="record_date",
                )
            if "category" in row_data:
                st.selectbox(
                    label="Select a category",
                    options=category_list,
                    index=get_index(category_list, row_data["category"]),
                    key="record_category",
                )

            st.form_submit_button(
                "Update", type="primary", on_click=update_record, args=(db_obj,)
            )

        # Delete Button
        st.button("Delete", on_click=delete_record, args=(db_obj,))
    else:
        st.success("Action performed successfully.")

def populate_table(
    db_obj: MongoDB, selected_month: str, selected_year: str, po: list, cl: list
) -> None:
    pipeline = [
        {
            "$match": {
                "date": {
                    "$regex": "{0}-{1}".format(selected_month, selected_year),
                    "$options": "i",
                }
            }
        },
        {
            "$group": {
                "_id": "$type",
                "records": {
                    "$push": {
                        "_id": "$_id",
                        "type": "$type",
                        "amount": "$amount",
                        "category": "$category",
                        "payment_from": "$payment_from",
                        "payment_to": "$payment_to",
                        "date": "$date",
                    }
                },
            }
        },
        {"$project": {"_id": 0, "category": "$_id", "records": 1}},
    ]
    result, records = db_obj.get_transaction_records_with_filters(pipeline)

    if isSuccess(result):
        total_balance = {}
        transaction_records = {}

        for record in records:
            transaction_records[record["category"]] = record["records"]

            for child_record in record["records"]:
                if record["category"] == "Income":
                    if child_record["payment_to"] in total_balance:
                        total_balance[child_record["payment_to"]] += child_record[
                            "amount"
                        ]
                    else:
                        total_balance[child_record["payment_to"]] = child_record[
                            "amount"
                        ]

                if record["category"] == "Payment":
                    if child_record["payment_from"] in total_balance:
                        total_balance[child_record["payment_from"]] -= child_record[
                            "amount"
                        ]
                    else:
                        total_balance[child_record["payment_from"]] = -child_record[
                            "amount"
                        ]

                if record["category"] == "Transfer":
                    if child_record["payment_from"] in total_balance:
                        total_balance[child_record["payment_from"]] -= child_record[
                            "amount"
                        ]
                    else:
                        total_balance[child_record["payment_from"]] = -child_record[
                            "amount"
                        ]
                    if child_record["payment_to"] in total_balance:
                        total_balance[child_record["payment_to"]] += child_record[
                            "amount"
                        ]
                    else:
                        total_balance[child_record["payment_to"]] = child_record[
                            "amount"
                        ]

        amount_column_config = {
            "amount": st.column_config.NumberColumn("amount", format="₹%.2f")
        }
        with st.container(height=200, border=False):
            for payment_option in total_balance:
                amount = total_balance[payment_option]
                content = "**{0} ₹{1:.2f}**".format(payment_option, amount)
                content_box = ":green-badge[{}]" if amount > 0 else ":red-badge[{}]"
                st.markdown(content_box.format(content))

        if not isEmptyList(transaction_records.get("Payment")):
            with st.expander(
                "Show all the Expense records", icon=":material/currency_rupee:"
            ):
                with st.container(height=300, border=False):
                    df = convert_to_df(transaction_records["Payment"])
                    drop_columns = (["type", "_id", "inv_type"] if "inv_type" in df.columns 
                                    else ["type", "_id"])
                    df.drop(drop_columns, axis="columns", inplace=True)
                    st.dataframe(
                        df,
                        height=300,
                        hide_index=True,
                        column_order=[
                            "date",
                            "amount",
                            "category",
                            "payment_from",
                            "spent_by",
                        ],
                        key="payment_data",
                        column_config=amount_column_config,
                        selection_mode="single-row",
                        on_select=lambda: show_data(
                            db_obj,
                            transaction_records["Payment"],
                            "payment_data",
                            po,
                            cl,
                        ),
                    )

        if not isEmptyList(transaction_records.get("Income")):
            with st.expander(
                "Show all the Income records", icon=":material/money_bag:"
            ):
                with st.container(height=300, border=False):
                    df = convert_to_df(transaction_records["Income"])
                    df.drop(["type", "_id"], axis="columns", inplace=True)
                    st.dataframe(
                        df,
                        height=300,
                        hide_index=True,
                        column_order=["date", "amount", "payment_to", "spent_by"],
                        key="income_data",
                        column_config=amount_column_config,
                        selection_mode="single-row",
                        on_select=lambda: show_data(
                            db_obj, transaction_records["Income"], "income_data", po, cl
                        ),
                    )

        if not isEmptyList(transaction_records.get("Transfer")):
            with st.expander(
                "Show all the Transfer records", icon=":material/swap_horiz:"
            ):
                with st.container(height=300, border=False):
                    df = convert_to_df(transaction_records["Transfer"])
                    df.drop(["type", "_id"], axis="columns", inplace=True)
                    st.dataframe(
                        df,
                        height=300,
                        hide_index=True,
                        column_order=[
                            "date",
                            "amount",
                            "payment_from",
                            "payment_to",
                            "spent_by",
                        ],
                        key="transfer_data",
                        column_config=amount_column_config,
                        selection_mode="single-row",
                        on_select=lambda: show_data(
                            db_obj,
                            transaction_records["Transfer"],
                            "transfer_data",
                            po,
                            cl,
                        ),
                    )
    else:
        st.error("Error: {0}".format(records), icon=":material/error:")

def show_transactions(db_obj: MongoDB, po: list, cl: list):

    st.header("Show Transaction", divider="blue", anchor=False)

    year_list, month_list, current_month_index = get_month_and_year_list()

    col1, col2 = st.columns(2)

    with col1:
        selected_month = st.selectbox(
            "Select a month", month_list, index=current_month_index
        )

    with col2:
        selected_year = st.selectbox("Select a year", year_list)

    clicked = st.button(label="Submit", key="show_transaction_button")

    if clicked:
        populate_table(db_obj, selected_month, selected_year, po, cl)


def main():
    db_obj = init_db()
    if db_obj is not None:

        payment_options = db_obj.get_payment_option_records()
        if isString(payment_options):
            st.error("Error: {0}".format(payment_options), icon=":material/error:")
            return
        elif isList(payment_options):
            payment_options = [i["pay_option_name"] for i in payment_options]

        category_list = db_obj.get_category_records()
        if isString(category_list):
            st.error("Error: {0}".format(category_list), icon=":material/error:")
            return
        elif isList(category_list):
            category_list = [i["category_name"] for i in category_list]

        show_transactions(db_obj, payment_options, category_list)


main()
