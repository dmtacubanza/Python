# -*- coding: utf-8 -*-
"""Plot1_DataViz.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/159OvwGlzPUL4qzfmNyY_tZPJ5lBJEBrs
"""

import pandas as pd
import numpy as np
import scipy
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df.info()

import plotly.graph_objects as go

df = pd.read_csv("fuel.csv")
df['PriceUpdatedDate'] = pd.to_datetime(df['PriceUpdatedDate'])
df_new = df.drop(['Address','Postcode','ServiceStationName','Suburb'], axis=1)

#date data type update
df_new['PriceUpdatedDate'] = pd.to_datetime(df_new['PriceUpdatedDate'])

#filter per 1 company, 1 fuel type
df_new = df_new[(df_new['Brand'] == 'Shell') & (df_new['FuelCode'] == 'P98')]

df_new

max_date = max(df_new['PriceUpdatedDate'])

df_current = df_new[(df_new['PriceUpdatedDate'] == max_date)]
df_current = df_current[(df_current['Price'] == max(df_current['Price']))]
df_current

max_date = max(df_new['PriceUpdatedDate'])
prev_date = max_date - datetime.timedelta(days=1)
#max_price = max(df_new['Price'])

df_previous = df_new[(df_new['PriceUpdatedDate'] == prev_date)]
df_previous = df_previous[(df_previous['Price'] == max(df_previous['Price']))]
df_previous

import datetime

# Get the current year and month
current_year = '2020' #datetime.datetime.now().year
current_month = '08' #datetime.datetime.now().month

df_average = df_new[(df_new['PriceUpdatedDate'].dt.year == current_year) & (df_new['PriceUpdatedDate'].dt.month == current_month)]
df_average

#visualization of bullet graph for monthly reference (e.g. current vs previous month, year 2019 vs 2020)
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+gauge+delta", value = max(df_new['Price']), #highest for the current day
    delta = {'reference': 139.9}, #last price of previous day
    domain = {'x': [0.25, 1], 'y': [0.08, 0.25]},
    title = {'text': "P98 Price Update"},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 300]},
        'threshold': {
            'line': {'color': "black", 'width': 2},
            'thickness': 0.75,
            'value': 120}, #lowest for the day
        'steps': [
            {'range': [0, 150], 'color': "gray"}, #average value for the current month
            {'range': [150, 250], 'color': "lightgray"}], #highest value for the month
        'bar': {'color': "black"}}))

!pip install Dash

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)