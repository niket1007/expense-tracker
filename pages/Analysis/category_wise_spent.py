import streamlit as st
import plotly.express as px

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
                "_id": "$category",
                "amount": { "$sum": "$amount" }
            }
        },
        {
            "$project": {
                "_id": 0,
                "category": "$_id",
                "amount": 1
            }
        },
        {
            "$sort": {"amount": -1}
        }
    ]
    status, transaction_records = db_obj.get_transaction_records_with_filters(pipeline)

    if isSuccess(status):
        with st.container(height=300, border=False):
            st.subheader("1) Category wise spending", divider="orange", anchor=False)
            st.data_editor(transaction_records,
                            disabled=True,
                            use_container_width=True,
                            column_config={
                                "value": st.column_config.NumberColumn(
                                        "value",
                                        format="₹%.2f"
                                    )
                            })
            
            # Pie Chart
            df = convert_to_df(transaction_records, ["category", "amount"])
            fig = px.pie(
                        data_frame=df, 
                        values='amount',
                        names='category', 
                        color_discrete_sequence=px.colors.sequential.Blues
                        )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)
    else:
        st.error("Error: {0}".format(transaction_records), icon=":material/error:")

