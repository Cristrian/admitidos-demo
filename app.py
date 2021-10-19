from dash import Dash, dcc, html

import callbacks
from data import data
from layouts import admitidos_live, admitidos_foto
from layouts.components import gen_download_button

app = Dash(__name__)

#Import Data
df = data.get_dataframe()

live_layout = [html.Div(admitidos_live.generate_layout('live')),
               html.Div(gen_download_button('live-btn_down', 'live-download-dataframe')),]

foto_layout = admitidos_foto.generate_layout('foto')


layout = html.Div([
    html.H1('Tablero Admitidos'),
    dcc.Tabs(
        [
        dcc.Tab(label='En Vivo', value='tab-en-vivo'),
        dcc.Tab(label='Fotografía', value='tab-foto'),
        ], 
        value='tab-en-vivo'),
    html.Div(id='page-content', children=live_layout),
    
])



app.layout = layout

callbacks.generate_graphics_callbacks(app, 'live', df)
callbacks.gen_download_callback(app, 'live', df)
callbacks.generate_graphics_callbacks(app, 'foto', df)

if __name__ == '__main__': 
    app.run_server()
