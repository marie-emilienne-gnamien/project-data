#Imports
import folium, branca
import json
import requests
import pandas as pd
from folium import JsCode
from folium.plugins import MarkerCluster
#Données
franceCenter = (46.539758, 2.430331)

response = requests.get("https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/json")
jsonResponse = response.json()
franceData = pd.DataFrame(jsonResponse)

franceData = franceData.query("gazole_prix.notna()")

franceMap = folium.Map(location=franceCenter, tiles='OpenStreetMap', zoom_start=6)
cm = branca.colormap.LinearColormap(['green','yellow','orange', 'red'], vmin=min(franceData["gazole_prix"]), vmax=max(franceData["gazole_prix"]))
franceMap.add_child(cm)

cluster = MarkerCluster().add_to(franceMap)

for _, row in franceData.iterrows():

    location = (row["geom"]["lat"], row["geom"]["lon"])

    folium.CircleMarker(
        location=location,
        radius=5,
        color=cm(float(row["gazole_prix"])),
        fill=True,
        fill_opacity=0.8,
        tooltip=f"{row['ville']} : {row['gazole_prix']}€",
        onclick="this._map.flyTo(this.getLatLng(), 16);"
    ).add_to(cluster)

franceMap.save('franceMap.html')

