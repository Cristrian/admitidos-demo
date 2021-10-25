import base64
import datetime
import io

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.html.H1 import H1
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

from data import data
from layouts import components

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

def parse_upload_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'imp' in filename:
            df = pd.DataFrame.from_dict(data.decrypt_dataframe(decoded))
        elif 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        dcc.Store(id='foto-stored-data', data=df.to_dict('records'))
    ])

def generate_graphics_callbacks(app: Dash, appname: str, df: pd.DataFrame):
    @app.callback(
        Output(f'{appname}-graphics-data', 'data'),
        [Input(f'{appname}-periodo-dropdown', 'value'),
        Input(f'{appname}-territorial-dropdown', 'value'),
        Input(f'{appname}-cetap-dropdown', 'value'),
        Input(f'{appname}-modalidad-dropdown', 'value'),
        Input(f'{appname}-metodologia-dropdown', 'value'),
        Input(f'{appname}-programa-dropdown', 'value')]
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

        #territorial Bar
        s_terr = filtered_df.groupby('direccion_territorial')['estado'].count()
        bar_terr = px.bar(s_terr, y=s_terr.index, x=s_terr.values)

        #Cetap Bar
        s_cetap = filtered_df.groupby('cetap')['estado'].count()
        bar_cetap = px.bar(s_cetap, y=s_cetap.index, x=s_cetap.values)

        #historico bar
        s_periodos = filtered_df.groupby('cod_periodo')['estado'].count()
        s_periodos.index = [
            str(periodo)[:-1]+'-I' if str(periodo)[-1]=='1'
            else
            str(periodo)[:-1]+'-II'
            for periodo in s_periodos.index
        ]
        bar_histor = px.bar(s_periodos, x=s_periodos.index, y=s_periodos.values)

        #Total_count

        count = filtered_df.shape[0]

        return {
            'programa-bar': bar_prog,
            'modalidad-pie': pie_mod,
            'metodologia-pie': pie_met,
            'territorial-bar': bar_terr,
            'cetap-bar': bar_cetap,
            'historico-bar': bar_histor,
            'total-count': count
        }

    return 'callbacks created'

def gen_foto_graphics_callbacks(app: Dash, appname: str):
    @app.callback(
        Output(f'{appname}-graphics-data', 'data'),
        Input(f'{appname}-stored-data', 'data'),
        [Input(f'{appname}-periodo-dropdown', 'value'),
        Input(f'{appname}-territorial-dropdown', 'value'),
        Input(f'{appname}-cetap-dropdown', 'value'),
        Input(f'{appname}-modalidad-dropdown', 'value'),
        Input(f'{appname}-metodologia-dropdown', 'value'),
        Input(f'{appname}-programa-dropdown', 'value')],
    )
    def generate_graphs(data, *values):
        #First, we're going to filter the dataframe
        #if values[0] is None:
        if data is None:
            raise PreventUpdate
        df = pd.DataFrame(data)
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

        #territorial Bar
        s_terr = filtered_df.groupby('direccion_territorial')['estado'].count()
        bar_terr = px.bar(s_terr, y=s_terr.index, x=s_terr.values)

        #Cetap Bar
        s_cetap = filtered_df.groupby('cetap')['estado'].count()
        bar_cetap = px.bar(s_cetap, y=s_cetap.index, x=s_cetap.values)

        #historico bar
        s_periodos = filtered_df.groupby('cod_periodo')['estado'].count()
        s_periodos.index = [
            str(periodo)[:-1]+'-I' if str(periodo)[-1]=='1'
            else
            str(periodo)[:-1]+'-II'
            for periodo in s_periodos.index
        ]
        bar_histor = px.bar(s_periodos, x=s_periodos.index, y=s_periodos.values)

        #Total_count

        count = filtered_df.shape[0]

        return {
            'programa-bar': bar_prog,
            'modalidad-pie': pie_mod,
            'metodologia-pie': pie_met,
            'territorial-bar': bar_terr,
            'cetap-bar': bar_cetap,
            'historico-bar': bar_histor,
            'total-count': count
        }

    @app.callback(
        Output(f'{appname}-output-upload', 'children'),
        Input(f'{appname}-upload-data', 'contents'),
        State(f'{appname}-upload-data', 'filename'),
        State(f'{appname}-upload-data', 'last_modified')
    )
    def update_output(contents, filenames, dates_mod):
        if contents is not None:
            print('hola Mundo')
            children =[
                parse_upload_contents(c, n, d) for c, n, d in
                zip(contents, filenames, dates_mod)]
        else:
            children = []
        return children
    return 'callbacks created'

def gen_download_callback(app: Dash, appname: str, df: pd.DataFrame):
    @app.callback(
        Output(f'{appname}-download-dataframe', 'data'),
        Input(f'{appname}-btn_down', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_data(n):
        return dict(content=data.encrypt_dataframe(df), filename='picture.imp')
    return None

def gen_upload_callback(app: Dash, appname: str):
    @app.callback(
        Output(f'{appname}-output-upload', 'children'),
        Input(f'{appname}-upload-data', 'contents'),
        State(f'{appname}-upload-data', 'filename'),
        State(f'{appname}-upload-data', 'last_modified')
    )
    def update_output(contents, filenames, dates_mod):
        if contents is not None:
            children =[
                parse_upload_contents(c, n, d) for c, n, d in
                zip(contents, filenames, dates_mod)]
        else:
            children = []
        return children
    return None

def plot_graphics_callback(app: Dash, appname: str):
    @app.callback(
        Output(f'{appname}-graphics', 'children'),
        [Input(f'{appname}-graphics-data', 'data'),
        Input(f'{appname}-pagination', 'active_page')]
    )
    def update_graphics(figures, pag):
        if not figures:
            raise PreventUpdate
        if pag == 1:
            graphics = [
                dbc.Row(
                    dbc.Col(dcc.Graph(
                        id=f'{appname}-admitidos-bar', 
                        figure=figures['programa-bar']
                    ))
                ),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(
                            id=f'{appname}-modalidad-pie',
                            figure=figures['modalidad-pie']
                        ), 
                        width='md-6'),
                    dbc.Col(
                        dcc.Graph(
                            id=f'{appname}-metodologia-pie',
                            figure=figures['metodologia-pie']
                        ), 
                        width='md-6'),
                ])
            ]
        elif pag==2:
            graphics = [
                dbc.Row(
                    dbc.Col(dcc.Graph(
                        id=f'{appname}-territorial-bar', figure=figures['territorial-bar']
                        )),
                ),
                dbc.Row(
                    dbc.Col(dcc.Graph(
                        id=f'{appname}-cetap-bar',
                        figure=figures['cetap-bar'])),
                ),
            ]
        elif pag==3:
            graphics = [
                dbc.Row(
                    components.generate_card(
                        id=f'{appname}-total-card',
                        color='blue',
                        card_title='Total Admitidos',
                        body=figures['total-count'])

                ),
                dbc.Row(
                    dcc.Graph(id=f'{appname}-historico-bar', figure=figures['historico-bar'])
                )
            ]
        return graphics

