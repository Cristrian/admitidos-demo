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

        #First, we're going to filter the dataframe
        filtered_df = df
        filters = {
            'periodo': values[0],
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
        bar_data = pd.Series(
                    
        )
        return values

    return 'callbacks created'