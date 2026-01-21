import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import folium

filename = "synthetic_disaster_events_2025.csv"
year = 2023
data = pd.read_csv(filename)
country = "Phillipines"
# dates = data['date']
# dates = dates.astype('str')



l = []
for i in range(len(data['date'])):
    l.append((int(str(data['date'][i][0:4])))) #modification de la colonne date, afin de juste garder les années
data['date'] = l
data.rename(columns={"date":"year"},inplace=True)


carte = px.scatter_geo(data,
                lon= 'longitude',
                lat= 'latitude' ,
                hover_name= 'location',
                hover_data=['year','disaster_type'],
                color= 'disaster_type'
                )
carte.update_layout(
    title= 'Worldwide natural disaster occurences documented between 2023 and 2025.'
)



aidP = px.histogram(data.query("year == @year"), x='location', color='aid_provided', barmode='group',height=600,title="The global amount of aid provided to countries.")

carte.show()