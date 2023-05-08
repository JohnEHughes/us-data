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
    toptier_codes_df = pd.DataFrame(toptier_codes_response.json().get('results')).head(20)
    return toptier_codes_df

st.dataframe(load_data())

st.bar_chart(load_data(), y='budget_authority_amount', x='agency_name')

response = requests.get("https://api.usaspending.gov/api/v2/agency/310/")

depart_name = response.json().get('name')
depart_abbr = response.json().get('abbreviation')
depart_toptier_code = response.json().get('toptier_code')


# response_df = pd.DataFrame(response.json())

st.write(depart_name)
st.write(depart_abbr)
st.write(depart_toptier_code)




# st.write(response.json())

