import streamlit as st

from utils import function_page, budget_function_years
from constants import FISCAL_YEARS


st.header("Department of the Treasury")

with st.expander("Show Budget Functions By Year"):

    with st.form(key="year_input"):

        year = st.selectbox(
            'PLEASE SELECT A FISCAL YEAR"',
            FISCAL_YEARS)

        submit = st.form_submit_button("Submit")
    if submit:
        function_page('020', year)



with st.expander("Show Budgets for All Years"):

    function_all_years_df = budget_function_years('020')
    col1, col2 = st.columns([1,1])
    list_budgets = []
    counter = 0
    for k,v in function_all_years_df.items():
        list_budgets.append(v)
        col1.metric(f"{k}", value=f"${v:,.2f}", delta=f"${(v - list_budgets[counter-1]):,.2f}")
        col2.metric("Percentage", value=f"{(v - list_budgets[counter-1]) /v*100:,.2f}%")
        counter+=1

    st.divider()
    st.line_chart(function_all_years_df)

# st.write(function_all_years_df)