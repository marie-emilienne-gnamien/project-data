import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import requests
import folium
import branca
from pathlib import Path
import data, carte, histograms

carte.generate_my_map()
histograms.generate_city_histogram()  # génère l'histogramme et le sauvegarde
years = [2026]
franceData = data.fetch_live_data()
app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1('Gas Prices in France', style={'textAlign': 'center', 'color': "#47793B"}),

    html.Div([
        html.Iframe(
            id='folium-map',
            srcDoc=open('src/pages/franceMap.html', 'r', encoding='utf-8').read(),
            style={'width': '100%', 'height': '600px', 'border': 'none'}
        )
        ], style={
        'width': '90%', 'margin': 'auto', 'border': '2px solid #47793B', 
        'borderRadius': '15px', 'overflow': 'hidden', 'boxShadow': '0 4px 15px rgba(0,0,0,0.2)'
    }),

    dcc.Graph(id='graph1'),
    dcc.Slider(id="year-slider", min=2024, max=2024, value=2024, marks={2024: '2024'})
])

@app.callback(
    Output('graph1', 'figure'),
    [Input('year-slider', 'value')]
)
def update_graph(selected_year):
    fig = px.histogram(franceData, x="gazole_prix", title="Les prix du gazole en France")
    return fig

if __name__ == '__main__':
    app.run(debug=True)