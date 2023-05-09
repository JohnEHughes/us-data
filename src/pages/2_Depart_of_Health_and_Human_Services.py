import streamlit as st

from utils import function_page
from constants import FISCAL_YEARS



st.header("Department of Health and Human Services")

with st.expander("Show Budget Functions By Year"):

    with st.form(key="year_input"):

        year = st.selectbox(
            'PLEASE SELECT A FISCAL YEAR"',
            FISCAL_YEARS)

        submit = st.form_submit_button("Submit")
    if submit:
        function_page('075', year)

