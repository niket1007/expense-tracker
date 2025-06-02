import streamlit as st
from pages.utility import *
import plotly.express as px

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
            per_category_spent = {}
            total_amount = 0
            for record in transaction_records:
                amount = float(record["amount"])
                category = record["category"]
                if category in per_category_spent:
                    per_category_spent[category] += amount
                else:
                    per_category_spent[category] = amount
                total_amount += amount
            
            with st.container(height=300, border=False):
                st.subheader("1) Category wise spending", divider="orange", anchor=False)
                st.data_editor(per_category_spent,
                               disabled=True,
                               use_container_width=True,
                               column_config={
                                   "value": st.column_config.NumberColumn(
                                            "value",
                                            format="₹%.2f"
                                        )
                               })
                
                # Pie Chart
                df = convert_to_df(per_category_spent, ["category", "amount"])
                fig = px.pie(
                            data_frame=df, 
                            values='amount',
                            names='category', 
                            color_discrete_sequence=px.colors.sequential.Blues
                            )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig)

