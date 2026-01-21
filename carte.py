#Imports

from pyproj import Transformer
import folium, branca
import json
import requests
import pandas as pd

#Données
franceCenter = (46.539758, 2.430331)

response = requests.get("https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/json")
jsonResponse = response.json()
franceData = pd.DataFrame(jsonResponse)

franceData = franceData.query("gazole_prix.notna()")


franceMap = folium.Map(location=franceCenter, tiles='OpenStreetMap', zoom_start=6)
cm = branca.colormap.LinearColormap(['green','yellow','orange', 'red'], vmin=min(franceData["gazole_prix"]), vmax=max(franceData["gazole_prix"]))
franceMap.add_child(cm) # add this colormap on the display

for i in range(len(franceData["latitude"])):
    location = (franceData["geom"].iloc[i]["lat"], franceData["geom"].iloc[i]["lon"])
    folium.Circle(location=location,
                        color= cm(float(franceData["gazole_prix"].iloc[i])),
                        Fill=False,
                        radius=5).add_to(franceMap)



franceMap.save('franceMap.html')

