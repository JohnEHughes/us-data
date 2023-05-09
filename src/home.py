import streamlit as st
import pandas as pd
import requests




st.header("US Data")

params = {
    'order': 'desc',
    'sort': 'percentage_of_total_budget_authority'
}

@st.cache_data
def load_data():
    toptier_codes_response = requests.get(f"https://api.usaspending.gov/api/v2/references/toptier_agencies", params=params)
    toptier_codes_df = pd.DataFrame(toptier_codes_response.json().get('results'))
    return toptier_codes_df


st.subheader("Top 10 Highest Budgets")
col1, col2 = st.columns([1,1])
total_budget = load_data()['budget_authority_amount'].sum()

def top_five(i):
    first_budget = load_data().budget_authority_amount[i:].max()
    first_budget_name = load_data().loc[load_data()['budget_authority_amount'] == first_budget, 'agency_name'].item()
    first_percent = first_budget / total_budget

    col1.metric(f"Number: {i+1} - {first_budget_name}", value=f"${first_budget:,}")
    col2.metric(f"Percentage", value=f"{first_percent:,.2%}")

for i in range(10):
    top_five(i)

df_visual = load_data()[['abbreviation', 'agency_name', 'toptier_code', 'budget_authority_amount']]
df_visual = df_visual.head(10).sort_values(by='budget_authority_amount', ascending=False)
df_visual = df_visual.rename(columns={'abbreviation': 'Abbrev.',
                          'agency_name': 'Agency Name',
                          'toptier_code': 'Top Tier Code',
                          'budget_authority_amount': 'Budget Amount',
                          }).set_index('Top Tier Code')

st.dataframe(df_visual)

st.bar_chart(load_data().head(10), y='budget_authority_amount', x='agency_name')







    









# response = requests.get("https://api.usaspending.gov/api/v2/agency/310/")

# depart_name = response.json().get('name')
# depart_abbr = response.json().get('abbreviation')
# depart_toptier_code = response.json().get('toptier_code')


# response_df = pd.DataFrame(response.json())

# st.write(depart_name)
# st.write(depart_abbr)
# st.write(depart_toptier_code)




# st.write(response.json())

