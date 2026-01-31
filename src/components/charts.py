import pandas as pd
import plotly.express as px
from pathlib import Path


MAJOR_CITIES = [
    'Paris','Marseille','Lyon','Toulouse','Nice',
    'Nantes','Strasbourg','Montpellier','Bordeaux','Lille'
]


def _find_column(df, keywords):
    """Retourne le nom de la première colonne contenant un des mots-clés donnés (insensible à la casse), ou None si aucune trouvée."""
    keys = [k.lower() for k in keywords]
    for col in df.columns:
        low = col.lower()
        if any(k in low for k in keys):
            return col
    return None


def generate_city_histogram_html(csv_path=None, out_html=None, cities=None):
    """Lit le fichier CSV des prix des carburants et génère un histogramme des prix moyens du gazole pour les grandes villes françaises."""
    if cities is None:
        cities = MAJOR_CITIES

    base = Path(__file__).resolve().parents[2]
    if csv_path is None:
        csv_path = base / 'prix-des-carburants-en-france.csv'
    else:
        csv_path = Path(csv_path)

    if out_html is None:
        out_html = base / 'city_histogram.html'
    else:
        out_html = Path(out_html)

    df = pd.read_csv(csv_path, sep=';', dtype=str)

    price_col = None
    for col in df.columns:
        low = col.lower()
        if 'prix' in low and 'gazole' in low and not any(x in low for x in ['mis', 'maj', 'mis à jour', 'mis_a_jour']):
            price_col = col
            break
    if price_col is None:
        price_col = _find_column(df, ['gazole', 'prix gazole', 'prix_gazole'])
    city_col = _find_column(df, ['ville', 'city']) or 'Ville'

    if price_col is None:
        raise RuntimeError('Could not find Gazole price column in CSV')

    # normalize and convert price values
    df[price_col] = df[price_col].astype(str).str.replace(',', '.').str.strip()
    df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
    df[city_col] = df[city_col].astype(str).str.strip()

    averages = []
    present_cities = []
    for city in cities:
        mask = df[city_col].str.lower().str.contains(city.lower(), na=False)
        vals = df.loc[mask, price_col].dropna().astype(float)
        if not vals.empty:
            present_cities.append(city)
            averages.append(vals.mean())

    if not present_cities:
        raise RuntimeError('No data found for the requested cities')

    fig = px.bar(x=present_cities, y=averages, labels={'x': 'Ville', 'y': 'Prix moyen Gazole (€)'} ,
                 title='Prix moyen du Gazole — Grandes villes françaises', template='plotly_white')

    html = fig.to_html(full_html=True, include_plotlyjs='cdn')
    out_html.write_text(html, encoding='utf-8')
    return out_html


if __name__ == '__main__':
    try:
        path = generate_city_histogram_html()
        print('Wrote city histogram to', path)
    except Exception as e:
        print('Error generating histogram:', e)