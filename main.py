import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import requests
import folium
import branca
from pathlib import Path

API_URL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/json"
MAJOR_CITIES = [
    'Paris','Marseille','Lyon','Toulouse','Nice',
    'Nantes','Strasbourg','Montpellier','Bordeaux','Lille'
]

def fetch_live_data():
    """Appelle l'API pour récupérer les données de prix des carburants en France."""
    response = requests.get(API_URL)
    return pd.DataFrame(response.json())

def generate_my_map():
    franceCenter = (46.539758, 2.430331)
    franceData = fetch_live_data()
    franceData = franceData.query("gazole_prix.notna()")

    franceMap = folium.Map(location=franceCenter, tiles='OpenStreetMap', zoom_start=6)
    cm = branca.colormap.LinearColormap(['green','yellow','orange', 'red'], 
                                        vmin=min(franceData["gazole_prix"]), 
                                        vmax=max(franceData["gazole_prix"]))
    franceMap.add_child(cm)

    for i in range(len(franceData)):
        location = (franceData["geom"].iloc[i]["lat"], franceData["geom"].iloc[i]["lon"])
        folium.Circle(location=location,
                      color=cm(float(franceData["gazole_prix"].iloc[i])),
                      fill=True, 
                      radius=500).add_to(franceMap) 

    listener_js = "<script>window.addEventListener('message', function(event) { ... });</script>"
    franceMap.get_root().html.add_child(folium.Element(listener_js))
    
    franceMap.save('src/pages/franceMap.html')
    return franceData

def generate_city_histogram():
    """Génère un histogramme des prix moyens du gazole pour les grandes villes françaises en utilisant les données de l'API."""
    franceData = fetch_live_data()
    
    city_col = None
    for col in franceData.columns:
        if 'ville' in col.lower() or 'city' in col.lower():
            city_col = col
            break
    
    if city_col is None:
        return None
    #calcul des moyennes
    averages = []
    present_cities = []
    for city in MAJOR_CITIES:
        mask = franceData[city_col].astype(str).str.lower().str.contains(city.lower(), na=False)
        vals = pd.to_numeric(franceData.loc[mask, 'gazole_prix'], errors='coerce').dropna()
        if not vals.empty:
            present_cities.append(city)
            averages.append(vals.mean())
    
    if not present_cities:
        return None
    
    fig = px.bar(
        x=present_cities, 
        y=averages, 
        labels={'x': 'Ville', 'y': 'Prix moyen Gazole (€)'},
        title='Prix moyen du Gazole — Grandes villes françaises',
        template='plotly_white'
    )
    
    html_str = fig.to_html(full_html=True, include_plotlyjs='cdn')
    out_path = Path(__file__).parent / 'src/pages/city_histogram.html'
    out_path.write_text(html_str, encoding='utf-8')
    return out_path

franceData = generate_my_map()
generate_city_histogram()  # génère l'histogramme et le sauvegarde
years = [2026]

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