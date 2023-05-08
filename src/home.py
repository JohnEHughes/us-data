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

st.dataframe(load_data().head(10).sort_values(by='budget_authority_amount', ascending=False))

st.bar_chart(load_data(), y='budget_authority_amount', x='agency_name')

col1, col2 = st.columns([1,1])

total_budget = load_data()['budget_authority_amount'].sum()

first_budget = load_data().budget_authority_amount.max()
first_budget_name = load_data().loc[load_data()['budget_authority_amount'] == first_budget, 'agency_name'].item()
first_percent = first_budget / total_budget

col1.metric(f"Highest - {first_budget_name}", value=f"${first_budget:,}")
col2.metric(f"Percentage - {first_budget_name}", value=f"{first_percent:,.2%}")



sec_budget = load_data().budget_authority_amount[1:].max()
sec_budget_name = load_data().loc[load_data()['budget_authority_amount'] == sec_budget, 'agency_name'].item()
sec_percent = sec_budget / total_budget


col1.metric(f"Second - {sec_budget_name}", value=f"${sec_budget:,}")
col2.metric(f"Percentage - {sec_budget_name}", value=f"{sec_percent:,.2%}")


third_budget = load_data().budget_authority_amount[2:].max()
third_budget_name = load_data().loc[load_data()['budget_authority_amount'] == third_budget, 'agency_name'].item()
third_percent = third_budget / total_budget


col1.metric(f"Third - {third_budget_name}", value=f"${third_budget:,}")
col2.metric(f"Percentage - {third_budget_name}", value=f"{third_percent:,.2%}")

four_budget = load_data().budget_authority_amount[3:].max()
four_budget_name = load_data().loc[load_data()['budget_authority_amount'] == four_budget, 'agency_name'].item()
four_percent = four_budget / total_budget


col1.metric(f"Forth - {four_budget_name}", value=f"${four_budget:,}")
col2.metric(f"Percentage - {four_budget_name}", value=f"{four_percent:,.2%}")










# response = requests.get("https://api.usaspending.gov/api/v2/agency/310/")

# depart_name = response.json().get('name')
# depart_abbr = response.json().get('abbreviation')
# depart_toptier_code = response.json().get('toptier_code')


# response_df = pd.DataFrame(response.json())

# st.write(depart_name)
# st.write(depart_abbr)
# st.write(depart_toptier_code)




# st.write(response.json())

