import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

filename = "synthetic_disaster_events_2025.csv"

# data = pd.read_csv(filename)
# data = data["City"].unique()

# print(data)
# # l = []
# # for la, lon in zip(data['lat'], data['lng']):
# #     l.append((la, lon))
# # data["coords"] = l

# # # print(data["coords"])

# # fig = px.choropleth(data, locations=data["coords"], color="Country",hover_name="Country",color_continuous_scale=px.colors.sequential.Plasma)
# # fig.show()