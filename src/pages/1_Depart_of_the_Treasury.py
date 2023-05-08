import streamlit as st
import pandas as pd
import requests

from utils import function_page


st.header("Department of the Treasury")


with st.form(key="year_input"):

    year = st.number_input("Year", min_value=2018, max_value=2023)
    submit = st.form_submit_button("Submit")
if submit:
    function_page('020', year)

