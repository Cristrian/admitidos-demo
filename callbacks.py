from dash import Dash
from dash.dependencies import Input, Output
import pandas as pd

def generate_graphics_callbacks(app: Dash, appname: str, df: pd.DataFrame):
    
    app.callback(
        Output(f'{appname}-admitidos-bar'),
        Output(f'{appname}-modalidad-pie'),
        Output(f'{appname}-metodologia-pie'),
        [Input(f'{appname}-periodo-dropdown'),
        Input(f'{appname}-territorial-dropdown'),
        Input(f'{appname}-cetap-dropdown'),
        Input(f'{appname}-modalidad-dropdown'),
        Input(f'{appname}-metodologia-dropdown'),
        Input(f'{appname}-programa-dropdown')],
    )
    def generate_graphs(*values):
        return values

    return 'callbacks created'