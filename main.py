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
_, departements_df, noms_departements = histograms.departement_histograms("Moselle")
years = [2026]
franceData = data.fetch_live_data()

app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1('Gazole Gas Prices in France', style={'textAlign': 'center', 'color': "#47793B"}),

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

    html.Iframe(
        id='histogram-moyenne',
        srcDoc=open("src/pages/city_histogram.html", "r").read(),  # lit le contenu HTML
        style={"width": "100%", "height": "500px", "border": "none"}
    ),

    html.Label('Département de votre choix :\n'),
    dcc.Dropdown(
        id="departement-dropdown",
        options=[{'label' : str(name) , 'value' : str(name)}
        for name in noms_departements
        if pd.notna(name)
        ],
        value="Moselle",
    ),
    html.Iframe(
        id='histogram-departement',
        srcDoc=open("src/pages/departement_histogram.html", "r").read(),  # lit le contenu HTML
        style={"width": "100%", "height": "600px", "border": "none"}
    )
])

@app.callback(
    Output('histogram-departement', 'srcDoc'),
    [Input('departement-dropdown', 'value')]
)
def update_histogram(selected_departement):
    out_path, _, _ = histograms.departement_histograms(selected_departement)

    with open(out_path, mode='r', encoding='utf-8') as f:
        content = f.read()
    return content

if __name__ == '__main__':
    app.run(debug=True)