import plotly.express as px
import data
import pandas as pd
from pathlib import Path

def generate_city_histogram():
    """Génère un histogramme des prix moyens du gazole pour les grandes villes françaises en utilisant les données de l'API."""
    franceData = data.fetch_live_data()
    
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
    for city in data.MAJOR_CITIES:
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
        template='plotly_white',
        color=present_cities
    )
    
    html_str = fig.to_html(full_html=True, include_plotlyjs='cdn')
    out_path = Path(__file__).parent / 'src/pages/city_histogram.html'
    out_path.write_text(html_str, encoding='utf-8')
    return out_path