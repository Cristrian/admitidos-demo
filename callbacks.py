import json
from dash import Dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

from data import data
def gen_query(col, value):
    """Generates a query to filter a Dataframe"""
    if (value is None) or (value == []):
        query = f'{col} != None'
    else:
        for i, val in enumerate(value):
            if i == 0:
                query = f'({col} == {val!r})'
            else:
                query = query + f' or ({col} == {val!r})'
    query = f'({query})'
    return query

def generate_graphics_callbacks(app: Dash, appname: str, df: pd.DataFrame):
    @app.callback(
        Output(f'{appname}-admitidos-bar', 'figure'),
        Output(f'{appname}-modalidad-pie', 'figure'),
        Output(f'{appname}-metodologia-pie', 'figure'),
        [Input(f'{appname}-periodo-dropdown', 'value'),
        Input(f'{appname}-territorial-dropdown', 'value'),
        Input(f'{appname}-cetap-dropdown', 'value'),
        Input(f'{appname}-modalidad-dropdown', 'value'),
        Input(f'{appname}-metodologia-dropdown', 'value'),
        Input(f'{appname}-programa-dropdown', 'value')],
    )
    def generate_graphs(*values):
        #First, we're going to filter the dataframe
        #if values[0] is None:
        print(values)
        filters_querys = [
            gen_query('cod_periodo', values[0]),
            gen_query('direccion_territorial', values[1]),
            gen_query('cetap', values[2]),
            gen_query('modalidad' ,values[3]),
            gen_query('metodologia' ,values[4]),
            gen_query('programa' ,values[5])
        ]


        #Now We're going do define the graphics data
        query = (
            f'{filters_querys[0]} and '
            f'{filters_querys[1]} and '
            f'{filters_querys[2]} and '
            f'{filters_querys[3]} and ' 
            f'{filters_querys[4]} and ' 
            f'{filters_querys[5]}' 
        )

        filtered_df = df.query(query)
        #Bar Data      
        programas = filtered_df['programa'].drop_duplicates()
        programas.index = [
            filtered_df.query(f'programa == {programa!r}').shape[0]
            for programa in programas
        ]

        #Admitidos programa figure
        bar_prog = px.bar(x=programas.index, y=programas.values)

        #Pie modalidad
        pie_mod = px.pie(filtered_df, names='modalidad')

        #Pie metodologia
        pie_met = px.pie(filtered_df, names='metodologia')

        return bar_prog, pie_mod, pie_met

    return 'callbacks created'

def gen_download_callback(app: Dash, appname: str):
    return None