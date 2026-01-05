import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

filename = "synthetic_disaster_events_2025.csv"

data = pd.read_csv(filename)

# dates = data['date']
# dates = dates.astype('str')

l = []
for i in range(len(data['date'])):
    l.append((int(str(data['date'][i][0:4])))) #modification de la colonne date, afin de juste garder les années
data['date'] = l


print(data['date'])
# print(dates.dtype)
# # l = []
# # for la, lon in zip(data['lat'], data['lng']):
# #     l.append((la, lon))
# # data["coords"] = l

# # # print(data["coords"])

# # fig = px.choropleth(data, locations=data["coords"], color="Country",hover_name="Country",color_continuous_scale=px.colors.sequential.Plasma)
# # fig.show()