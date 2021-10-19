import json
from dash import Dash
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

from data import data

def generate_graphics_callbacks(app: Dash, appname: str, df: pd.DataFrame):
    df = data.get_dataframe()
    @app.callback(
        Output('test-out12', 'children'),
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
        filters = {
            'cod_periodo': values[0],
            'direccion_territorial': values[1],
            'cetap': values[2],
            'modalidad': values[3],
            'metodologia': values[4],
            'programa': values[5]
        }


        
        for col in filters:
            if filters[col] is None:
                filtered_df.query(f'{col} != -1', inplace=True)
            else:
                filtered_df = filtered_df[filtered_df[col].isin(filters[col])]

        #Now We're going do define the graphics data
        #Bar Data      
        programas = filtered_df['programa'].drop_duplicates()
        programas.index = [
            filtered_df.query(f'programa == {programa!r}').shape[0]
            for programa in programas
        ]

        #Pie1 Data
        modalidades = filtered_df['modalidad'].drop_duplicates()
        modalidades.index = [
            filtered_df.query(f'modalidad == {modalidad!r}').shape[0]
            for modalidad in modalidades
        ]

        #Pie2 Data
        metodologias = filtered_df['metodologia'].drop_duplicates()
        metodologias.index = [
            filtered_df.query(f'metodologia == {metodologia!r}').shape[0]
            for metodologia in metodologias
        ]

        #Admitidos programa figure
        bar_prog = px.bar(x=[1,2,3], y=[4,5,6])

        #Pie modalidad
        pie_mod = px.pie(filtered_df, names='modalidad')

        #Pie metodologia
        pie_met = px.pie(filtered_df, names='metodologia')

        return values, bar_prog, pie_mod, pie_met

    return 'callbacks created'