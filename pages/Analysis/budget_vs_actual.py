import streamlit as st
from pages.utility import *

def main(db_obj: object, custom_db: object, data: object):

    transaction_filter = {
            "date": {
                "$regex": "{0}-{1}".format(data["month"], data["year"]), 
                "$options": "i"
                },
            "type": "Payment"
            }
    budget_filter = {
        "month": data["month"],
        "year": data["year"]
    }
    transaction_records = custom_db.fetch_transaction_records_with_filters(
        db_obj, transaction_filter)
    if not isList(transaction_records):
        custom_db.clear_cache("Cache_Resource")
        st.error("Error: {0}".format(transaction_records), icon=":material/error:")
        return
    
    budget_record = custom_db.fetch_budget_record(db_obj, budget_filter)
    if not isList(budget_record):
        custom_db.clear_cache("Cache_Resource")
        st.error("Error: {0}".format(budget_record), icon=":material/error:")
        return

    if not isEmptyList(budget_record) and not isEmptyList(transaction_records):
        transformed_budget = {}
        for element in convert_to_json(budget_record[0]["budget"]):
            transformed_budget[element["category_name"]] = int(element["budget"])
        
        combined_data = {}
        for record in transaction_records:
            category = record["category"]
            amount = int(record["amount"])
            if category in combined_data:
                combined_data[category]["Actual"] += amount
            else:
                combined_data[category] = {"Actual": amount, "Expected": transformed_budget.get(category, 0)}
        
        transform_combined_data = []
        for record in combined_data:
            transform_combined_data.append({
                "Category": record,
                "Actual": combined_data[record]["Actual"],
                "Budget": combined_data[record]["Expected"]
            })

        st.table(transform_combined_data)

    
