import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_resource
def get_data():
    data = pd.read_csv("file.csv")

    data['data'] = pd.to_datetime(data['data'], format='%d/%m/%Y')

    return data


def get_wettest_day(data):
    wettest = data[data['precip'] == data['precip'].max()].reset_index()

    return wettest['data'][0]


def get_wettest_month(data):
    grouped = data.groupby([data['data'].dt.year, data['data'].dt.month])
    dictionary = grouped['precip'].sum().to_dict()

    wettest = max(dictionary, key=dictionary.get)

    return {
        'year': wettest[0],
        'month': wettest[1]
    }


def get_wettest_year(dados):
    grouped = dados.groupby(dados['data'].dt.year)
    dictionary = grouped['precip'].sum().to_dict()

    year = max(dictionary, key=dictionary.get)

    return year


def get_year_mean_temperature(data):
    return data.groupby(data['data'].dt.year)['temp_media'].mean().to_dict()


def get_year_mean_plot(mean):
    fig = px.line(x=mean.keys(), y=mean.values(), labels={
        'x': 'Month',
        'y': 'Mean temperature'
    }, title='Year mean temperature')
    fig.update_xaxes(type='category')

    return fig


def get_minimum_mean(data, month) -> dict[int, float]:
    filtered = data[(data['data'].dt.month == month)]
    minimum_mean = filtered.groupby(data['data'].dt.year)[
        'minima'].mean().to_dict()

    return minimum_mean


def create_temperature_trends_chart(data):
    data['date'] = pd.to_datetime(data['data'])

    fig = px.line(data, x='date', y=['maxima', 'minima'],
                  labels={'value': 'Temperature (°C)', 'date': 'Date'},
                  title='Temporal Trends of Maximum and Minimum Temperatures')

    fig.update_layout(legend=dict(
        yanchor="top", y=0.99, xanchor="left", x=0.01))
    return fig


def correlation_heatmap(data):
    correlation = data.corr()

    fig = px.imshow(correlation, text_auto=True)

    return fig


def calculate_weather_metrics(data_file):
    data = pd.read_csv(data_file)

    metrics = {
        'Maximum Temperature': {
            'Mean': data['maxima'].mean(),
            'Median': data['maxima'].median(),
            'Maximum': data['maxima'].max(),
            'Minimum': data['maxima'].min(),
        },
        'Minimum Temperature': {
            'Mean': data['minima'].mean(),
            'Median': data['minima'].median(),
            'Maximum': data['minima'].max(),
            'Minimum': data['minima'].min(),
        },
        'Precipitation': {
            'Mean': data['precip'].mean(),
            'Median': data['precip'].median(),
            'Maximum': data['precip'].max(),
            'Minimum': data['precip'].min(),
        },
        'Wind': {
            'Mean': data['vel_vento'].mean(),
            'Median': data['vel_vento'].median(),
            'Maximum': data['vel_vento'].max(),
            'Minimum': data['vel_vento'].min(),
        }
    }

    return metrics
