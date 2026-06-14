import streamlit as st

# Pages
from pages.utility import *

# MongoDb
from mongodb.mongodb import MongoDB

def main(db_obj: MongoDB, data: object):
    pipeline = [
        {
        "$match": {
            "date": {
                "$regex": "{0}-{1}".format(data["month"], data["year"]),
                "$options": "i"
                },
            "type": "Payment"
            }
        },
        {
            "$group": {
                "_id": {
                    "spent_by": "$spent_by",
                    "category": "$category"
                    },
                "total_amount": { "$sum": "$amount" }
            }
        },
        {
            "$project": {
                "_id": 0,
                "spent_by": "$_id.spent_by",
                "category": "$_id.category",
                "total_amount": 1
            }
        },
        {
            "$sort": {"total_amount": -1}
        }
    ]
    

    status, transaction_records = db_obj.get_transaction_records_with_filters(pipeline)

    if isSuccess(status):
        per_user_total_spent = {}
        per_category_per_user_spent = {}
        user_column = set()

        for record in transaction_records:
            name = record["spent_by"]
            category = record["category"]
            if name in per_user_total_spent:
                per_user_total_spent[name] += record["total_amount"]
            else:
                per_user_total_spent[name] = record["total_amount"]
            
            if name in per_category_per_user_spent:
                per_category_per_user_spent[name][category] = record["total_amount"]
            else:
                per_category_per_user_spent[name] = {category: record["total_amount"]}
            
            user_column.add(name)

        # Per user spending for selected month and year
        with st.container(height=200, border=False):
            st.subheader("1) Per user total spending", divider="orange", anchor=False)
            st.data_editor(per_user_total_spent,
                            disabled=True,
                            use_container_width=True,
                            column_config={
                                "value": st.column_config.NumberColumn(
                                        "value",
                                        format="₹%.2f"
                                    )
                            })

        # Per user spending on each category
        with st.container(height=200, border=False):
            st.subheader("2) Per category user spending", divider="orange", anchor=False)
            column_configs = {
                key: st.column_config.NumberColumn(
                    label= key.capitalize(),
                    default=0,
                    format="₹%.2f"
                ) for key in user_column
            }

            st.data_editor(per_category_per_user_spent,
                            disabled=True,
                            use_container_width=True,
                            column_config=column_configs)
    else:
        st.error("Error: {0}".format(transaction_records), icon=":material/error:")


