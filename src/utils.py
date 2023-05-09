import streamlit as st
import pandas as pd
import requests

from constants import FISCAL_YEARS

def load_data(code, params):
    toptier_codes_response = requests.get(f"https://api.usaspending.gov/api/v2/agency/{code}/budget_function/", params=params)
    toptier_codes_df = pd.DataFrame(toptier_codes_response.json()['results'])
    return toptier_codes_df

def load_data_year(code, year):
    params = {
        'fiscal_year': year,
    }

    toptier_codes_response = requests.get(f"https://api.usaspending.gov/api/v2/agency/{code}/budget_function/", params=params)
    toptier_codes_df = pd.DataFrame(toptier_codes_response.json()['results'])
    toptier_codes_df['year'] = year

    toptier_codes_df = toptier_codes_df[['name', 'obligated_amount', 'year']]
    toptier_codes_df = toptier_codes_df.sort_values(by='obligated_amount', ascending=False)
    toptier_codes_df = toptier_codes_df.rename(columns={'obligated_amount': 'Budget Amount', 'name': 'Function', 'year': 'Year'})

    return toptier_codes_df

def function_page(code, year):
    params = {
        'fiscal_year': year,
    }

    data = load_data(code, params)

    total_budget = data['obligated_amount'].sum()
    st.subheader("Total Budget")
    st.text(f"${total_budget:,}")

    df_visual = data[['name', 'obligated_amount']]
    df_visual = df_visual.sort_values(by='obligated_amount', ascending=False)
    df_visual = df_visual.rename(columns={'obligated_amount': 'Budget Amount', 'name': 'Function'}).set_index('Budget Amount')

    st.divider()
    st.subheader("Budget Functions")

    total_budget = data['obligated_amount'].sum()

    def metric_list(i):
        first_budget = data.obligated_amount[i:].max()
        first_budget_name = data.loc[data['obligated_amount'] == first_budget, 'name'].item()
        first_percent = first_budget / total_budget
        st.subheader(f"{i+1} - {first_budget_name}")
        st.write(f"${first_budget:,}")
        st.text(f"Percentage - {first_percent:,.2%}")

    for i in range(data.shape[0]):
        metric_list(i)


def budget_function_years(code):
    function_data = pd.DataFrame([['name', 'obligated_amounts']])
    budget_year_dict= {}
    for year in FISCAL_YEARS:
        df = load_data_year(code, year)
        budget_year = df[df['Year'] == year]['Budget Amount'].sum()
        budget_year_dict[year] = budget_year
        # function_data =  pd.concat([df, function_data])
    return budget_year_dict

