import logic
import const
import pandas as pd
from streamlit.delta_generator import DeltaGenerator


def filter(dg: DeltaGenerator, data):
    col_min, col_max, col_columns = dg.columns([1, 1, 3])

    min = data['data'].min()
    max = data['data'].max()

    init_date = pd.to_datetime(col_min.date_input(
        'initial date', value=min, min_value=min, max_value=max))
    end_date = pd.to_datetime(col_max.date_input(
        'final date', value=max, min_value=min, max_value=max))
    columns = col_columns.selectbox('categorias', const.columns.keys())
    columns = ['data'] + const.columns[columns]

    return init_date, end_date, columns


def table(dg: DeltaGenerator, data):
    init_date, end_date, columns = filter(dg, data)

    data = data[data['data'].between(
        init_date, end_date)]

    visible_data = data[columns]
    dg.dataframe(visible_data, hide_index=True, use_container_width=True)

    return data


def wettest(dg: DeltaGenerator, data):

    wettest_day(dg, data)
    dg.subheader("")

    wettest_month(dg, data)
    dg.subheader("")

    wettest_year(dg, data)


def wettest_day(dg: DeltaGenerator, data):
    dg.subheader("Wettest day", divider="rainbow")
    col_year, col_month, col_day = dg.columns(3)

    wettest = logic.get_wettest_day(data)
    col_year.metric("Year", wettest.year)
    col_month.metric("Month", wettest.month)
    col_day.metric("Day", wettest.day)


def wettest_month(dg: DeltaGenerator, data):
    dg.subheader("Wettest month", divider="rainbow")
    col_month, col_year = dg.columns(2)

    wettest = logic.get_wettest_month(data)
    col_month.metric("Month", wettest['month'])
    col_year.metric("Year", wettest['year'])


def wettest_year(dg: DeltaGenerator, data):
    dg.subheader("Wettest year", divider="rainbow")
    col_year = logic.get_wettest_year(data)
    dg.metric("Year", col_year)


def year_mean_temperature(dg: DeltaGenerator, data):
    dg.header("Year mean temperature", divider="rainbow")

    col_json, _, col_plot = dg.columns([5, 1, 12])

    mean = logic.get_year_mean_temperature(data)

    container_json = col_json.container(height=400)
    container_json.json(mean)

    col_plot.plotly_chart(logic.get_year_mean_plot(
        mean), use_container_width=True)


def correlation(dg: DeltaGenerator, data):
    dg.header("Correlation", divider="rainbow")

    dg.plotly_chart(logic.correlation_heatmap(data))


def temporal_trends(dg: DeltaGenerator, data):
    dg.header("Temporal trends", divider="rainbow")
    dg.plotly_chart(logic.create_temperature_trends_chart(
        data), use_container_width=True)
