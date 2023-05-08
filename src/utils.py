import streamlit as st
import pandas as pd
import requests


def function_page(code, year):
    params = {
        'fiscal_year': year,
    }

    # @st.cache_data
    def load_data():
        toptier_codes_response = requests.get(f"https://api.usaspending.gov/api/v2/agency/{code}/budget_function/", params=params)
        toptier_codes_df = pd.DataFrame(toptier_codes_response.json()['results'])
        return toptier_codes_df

    total_budget = load_data()['gross_outlay_amount'].sum()
    st.subheader("Total Budget")
    st.text(f"${total_budget:,}")
    print(year)
    st.write(year)
    df_visual = load_data()[['name', 'gross_outlay_amount']]
    df_visual = df_visual.sort_values(by='gross_outlay_amount', ascending=False)
    df_visual = df_visual.rename(columns={'gross_outlay_amount': 'Budget Amount', 'name': 'Function'}).set_index('Budget Amount')

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
