import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import requests
import folium
import branca

def generate_my_map():
    franceCenter = (46.539758, 2.430331)
    response = requests.get("https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/json")
    jsonResponse = response.json()
    franceData = pd.DataFrame(jsonResponse)
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
    
    franceMap.save('franceMap.html')
    return franceData

franceData = generate_my_map()
years = [2026] #on va le changer plus tard

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Gas Prices in France', style={'textAlign': 'center', 'color': "#47793B"}),

    html.Div([
        html.Iframe(
            id='folium-map',
            srcDoc=open('franceMap.html', 'r', encoding='utf-8').read(),
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