from dash import Dash, dcc, html
from dash.dcc.Store import Store
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import callbacks
from data import data
from layouts import admitidos
from layouts.components import gen_download_button, gen_upload_box

app = Dash(__name__, suppress_callback_exceptions=True)

#Import Data
df_live = data.get_dataframe()

live_layout = [html.Div(admitidos.generate_layout('live')),
               html.Div(gen_download_button('live-btn_down', 'live-download-dataframe')),
               html.Div(dbc.Pagination(id='live-pagination', max_value=3, active_page=1))]

foto_layout = [
    html.Div(gen_upload_box('foto-upload-data', 'foto-output-upload')),
    html.Div(admitidos.generate_layout('foto')),
    html.Div(dbc.Pagination(id='foto-pagination', max_value=3, active_page=1))
]


app.layout = html.Div([
    html.H1('Tablero Admitidos'),
    dcc.Tabs(
        [
        dcc.Tab(label='En Vivo', value='tab-en-vivo'),
        dcc.Tab(label='Fotografía', value='tab-foto'),
        ],
        id='tabs-component', 
        value='tab-en-vivo'
    ),
    html.Div(id='page-content'),
    
])

callbacks.generate_graphics_callbacks(app, 'live', df_live)
callbacks.gen_download_callback(app, 'live', df_live)
callbacks.gen_foto_graphics_callbacks(app, 'foto')


@app.callback(
    Output('live-graphics', 'children'),
    Input('live-pagination', 'active_page')
)
def update_graphics(pag):
    print('Hola Mundo')
    return admitidos.gen_graphics_layout(pag, 'live')

@app.callback(
    Output('foto-graphics', 'children'),
    Input('foto-pagination', 'active_page')
)
def update_graphics(pag):
    print('Hola Mundo')
    return admitidos.gen_graphics_layout(pag, 'foto')

@app.callback(
    Output('page-content', 'children'),
    Input('tabs-component', 'value')
)
def render_content(tab):
    if tab == 'tab-en-vivo':
        content = live_layout
    elif tab == 'tab-foto':
        content = foto_layout
    return content


if __name__ == '__main__': 
    app.run_server(debug=True)
