import streamlit as st
import logic
import cards


def config_page():
    st.set_page_config(layout="wide", page_title="Meteorology Dashboard")
    st.header('Data')


config_page()
data = logic.get_data()


col_table, _, col_wettest,  = st.columns([16, 1, 7])

data = cards.table(col_table, data)
cards.wettest(col_wettest, data)

col_year_mean = st.columns(1)[0]
cards.year_mean_temperature(col_year_mean, data)

col_correlation = st.columns(1)[0]
cards.correlation(col_correlation, data)
