from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts import components
from data import data
test_dropdown = {'Valor 1': 1, 'Valor 2': 2}
def generate_layout(appname):

    dropdowns_data = data.get_dropdown_data()
    dropdowns = [
        dbc.Row([
            dbc.Col(
                components.generate_dropdown(
                    id=f'{appname}-periodo-dropdown',
                    title='Periodo',
                    dropdown_data=dropdowns_data['periodo-dropdown'],
                )
            ),
            dbc.Col(
                components.generate_dropdown(
                    id=f'{appname}-territorial-dropdown',
                    title='Dirección Territorial',
                    dropdown_data=dropdowns_data['territorial-dropdown'],
                )
            ),
            dbc.Col(
                components.generate_dropdown(
                    id=f'{appname}-cetap-dropdown',
                    title='CETAP',
                    dropdown_data=dropdowns_data['cetap-dropdown'],
                )
            ),
        ]),
        dbc.Row([
            dbc.Col(
                components.generate_dropdown(
                    id=f'{appname}-modalidad-dropdown',
                    title='Modalidad',
                    dropdown_data=dropdowns_data['modalidad-dropdown'],
                )
            ),
            dbc.Col(
                components.generate_dropdown(
                    id=f'{appname}-metodologia-dropdown',
                    title='Metodología',
                    dropdown_data=dropdowns_data['metodologia-dropdown'],
                )
            ),
            dbc.Col(
                components.generate_dropdown(
                    id=f'{appname}-programa-dropdown',
                    title='Programa',
                    dropdown_data=dropdowns_data['programa-dropdown'],
                )
            ),
        ]),
    ]

    graphics = [
        dbc.Row(
            dcc.Graph(id=f'{appname}-admitidos-bar')
        ),
        dbc.Row([
            dbc.Col(dcc.Graph(id=f'{appname}-modalidad-pie')),
            dbc.Col(dcc.Graph(id=f'{appname}-metodologia-pie')),
        ])
    ]

    layout = dbc.Container(
        [
            html.Div(dropdowns),
            html.Div(graphics),
        ],
        fluid=True
    )
    
    return layout

