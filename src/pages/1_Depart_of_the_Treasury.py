import streamlit as st
import pandas as pd
import requests



st.header("Department of the Treasury")

params = {
    'fiscal_year': 2023,
    'limit': 12,
}

@st.cache_data
def load_data():
    toptier_codes_response = requests.get("https://api.usaspending.gov/api/v2/agency/020/budget_function", params=params)
    toptier_codes_df = pd.DataFrame(toptier_codes_response.json()['results'])
    return toptier_codes_df

# fiscal_year (optional, number) The desired appropriations fiscal year. Defaults to the current FY.
# filter (optional, string) This will filter the Budget Function by their name to those matching the text.
# order (optional, enum[string]) Indicates what direction results should be sorted by. Valid options include asc for ascending order or desc for descending order.
# Default: desc
# Members
# desc
# asc
# sort (optional, enum[string]) Optional parameter indicating what value results should be sorted by.
# Default: obligated_amount
# Members
# name
# obligated_amount
# gross_outlay_amount
# page (optional, number) The page number that is currently returned.
# Default: 1
# limit (optional, number) How many results are returned.
# Default: 10

total_budget = load_data()['gross_outlay_amount'].sum()
st.subheader("Total Budget")
st.text(f"${total_budget:,}")


df_visual = load_data()[['name', 'gross_outlay_amount']]
df_visual = df_visual.sort_values(by='gross_outlay_amount', ascending=False)
df_visual = df_visual.rename(columns={'gross_outlay_amount': 'Budget Amount',
                          'name': 'Function'
                          }).set_index('Budget Amount')

st.divider()
st.subheader("Budget Functions")

total_budget = load_data()['gross_outlay_amount'].sum()

def metric_list(i):
    first_budget = load_data().gross_outlay_amount[i:].max()
    first_budget_name = load_data().loc[load_data()['gross_outlay_amount'] == first_budget, 'name'].item()
    first_percent = first_budget / total_budget
    st.subheader(f"{i+1} - {first_budget_name}")
    st.write(f"${first_budget:,}")
    st.text(f"Percentage - {first_percent:,.2%}")

for i in range(load_data().shape[0]):
    metric_list(i)
