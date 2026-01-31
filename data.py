import json
import requests
import pandas as pd

API_URL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/json"
MAJOR_CITIES = [
    'Paris','Marseille','Lyon','Toulouse','Nice',
    'Nantes','Strasbourg','Montpellier','Bordeaux','Lille'
]

def fetch_live_data():
    """Appelle l'API pour récupérer les données de prix des carburants en France."""
    response = requests.get(API_URL)
    return pd.DataFrame(response.json())
