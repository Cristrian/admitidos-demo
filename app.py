from dash import Dash, dcc, html
from dash.html.H1 import H1

import callbacks
from layouts import admitidos_live, admitidos_foto
app = Dash(__name__)

#Import Data


live_layout = admitidos_live.generate_layout('live')
foto_layout = admitidos_foto.generate_layout('foto')

layout = html.Div([
    html.H1('Tablero Admitidos'),
    dcc.Tabs(
        [
        dcc.Tab(label='En Vivo', value='tab-en-vivo'),
        dcc.Tab(label='Fotografía', value='tab-foto'),
        ], 
        value='tab-en-vivo'),
    html.Div(id='page-content', children=live_layout)
])
app.layout = layout


if __name__ == '__main__':
    
    app.run_server()
