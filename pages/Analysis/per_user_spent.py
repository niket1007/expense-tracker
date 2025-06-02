import streamlit as st
from pages.utility import *

def main(db_obj: object, custom_db: object, data: object):

    filters = {
            "date": {
                "$regex": "{0}-{1}".format(data["month"], data["year"]), 
                "$options": "i"
                },
            "type": "Payment"
            }
    transaction_records = custom_db.fetch_transaction_records_with_filters(db_obj, filters)

    if not isList(transaction_records):
        custom_db.clear_cache("Cache_Resource")
        st.error("Error: {0}".format(transaction_records), icon=":material/error:")
    else:
        if not isEmptyList(transaction_records):
            
            # Per user spending for selected month and year
            per_user_spent = {}

            for record in transaction_records:
    
                if record["spent_by"] in per_user_spent:
                    per_user_spent[record["spent_by"]] += float(record["amount"])
                else:
                    per_user_spent[record["spent_by"]] = float(record["amount"])
            
            with st.container(height=200, border=False):
                st.subheader("1) Per user total spending", divider="orange", anchor=False)
                st.data_editor(per_user_spent,
                               disabled=True,
                               use_container_width=True,
                               column_config={
                                   "value": st.column_config.NumberColumn(
                                            "value",
                                            format="₹%.2f"
                                        )
                               })

            # Per user spending on each category
            per_user_per_category_spent = {}
            user_column = []
            for record in transaction_records:
                user = record["spent_by"]
                amount = float(record["amount"])
                category = record["category"]
                user_column.append(user)
                if user in per_user_per_category_spent:
                    if record["category"] in per_user_per_category_spent[user]:
                        per_user_per_category_spent[user][category] += amount
                    else:
                        per_user_per_category_spent[user][category] = amount
                else:
                    per_user_per_category_spent[user] = {category: amount}
            
            with st.container(height=200, border=False):
                st.subheader("2) Per category user spending", divider="orange", anchor=False)
                column_configs = {
                    key: st.column_config.NumberColumn(
                        label= key.capitalize(),
                        default=0,
                        format="₹%.2f"
                    ) for key in user_column
                }

                st.data_editor(per_user_per_category_spent,
                               disabled=True,
                               use_container_width=True,
                               column_config=column_configs)


