from dash import Dash
from dash.dependencies import Input, Output
import pandas as pd

def generate_graphics_callbacks(app: Dash, appname: str, df: pd.DataFrame):
    
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
        return values

    return 'callbacks created'