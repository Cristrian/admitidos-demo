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

    graphics = html.Div(id=f'{appname}-graphics')

    layout = dbc.Container(
        [
            html.Div(dropdowns),
            html.Div(graphics),
        ],
        fluid=True
    )
    
    return layout


"""def gen_graphics_layout(page: int, appname):
    if page == 1:
        graphics = [
            dbc.Row(
                dbc.Col(dcc.Graph(id=f'{appname}-admitidos-bar', ))
            ),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id=f'{appname}-modalidad-pie'), width='md-6'),
                dbc.Col(
                    dcc.Graph(id=f'{appname}-metodologia-pie'), width='md-6'),
            ])
        ]
    elif page == 2:
        graphics = [
            dbc.Row(
                dbc.Col(dcc.Graph(id=f'{appname}-territorial-bar')),
            ),
            dbc.Row(
                dbc.Col(dcc.Graph(id=f'{appname}-cetap-bar')),
            ),
        ]
    elif page == 3:
        graphics = [
            dbc.Row(
                components.generate_card(
                    id=f'{appname}-total-card',
                    color='blue',
                    card_title='Total Admitidos')
            ),
            dbc.Row(
                dcc.Graph(id=f'{appname}-historico-bar')
            )
        ]
    return graphics
"""