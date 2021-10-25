from dash import Dash, dcc, html
from dash.dcc.Store import Store
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import callbacks
from data import data
from layouts import admitidos, components
from layouts.components import gen_download_button, gen_upload_box

app = Dash(__name__, suppress_callback_exceptions=True)

#Import Data
df_live = data.get_dataframe()

live_layout = [dcc.Store(id='live-graphics-data'),
               html.Div(admitidos.generate_layout('live')),
               html.Div(gen_download_button('live-btn_down', 'live-download-dataframe')),
               html.Div(dbc.Pagination(id='live-pagination', max_value=3, active_page=1))]

foto_layout = [
    dcc.Store(id='foto-graphics-data'),
    html.Div(gen_upload_box('foto-upload-data', 'foto-output-upload')),
    html.Div(admitidos.generate_layout('foto')),
    html.Div(dbc.Pagination(id='foto-pagination', max_value=3, active_page=1))
]


app.layout = dbc.Container(
    [
       
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
    ],
    fluid=True
)

callbacks.generate_graphics_callbacks(app, 'live', df_live)
callbacks.gen_download_callback(app, 'live', df_live)
callbacks.gen_foto_graphics_callbacks(app, 'foto')
callbacks.plot_graphics_callback(app, 'live')
callbacks.plot_graphics_callback(app, 'foto')

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
