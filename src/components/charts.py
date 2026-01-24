import plotly.express as px

def create_price_histogram(df):
    """Crée un histogramme interactif des prix du carburant.
    """
    carburants = df['prix_nom'].unique()
    
    fig = px.histogram(
        df[df['prix_nom'] == carburants[0]],
        x='region',
        y='prix_valeur',
        histfunc='avg',
        color="region",
        title=f"Prix moyen par région : {carburants[0]}",
        labels={'prix_valeur': 'Prix moyen (€)', 'region': 'Région'},
        height=600,
        template="plotly_white"
    )
    
    buttons = []
    for fuel in carburants:
        df_fuel = df[df['prix_nom'] == fuel]
        
        buttons.append(dict)(
            method='restyle',
            label=fuel,
            args=[{'y': [df_fuel['prix_valeur'].mean()],
                   'x': [df_fuel['region']].mean().index(),
                   'type': 'histogram'},
                  {'title': f"Prix moyen par région : {fuel}"}]
        )
        
    fig.update_layout(
        updatemenus=[dict(
            buttons=buttons,
            direction='down',
            showactive=True,
            x=0.1,
            xanchor='left',
            y=1.15,
            yanchor='top'
        )],
        xaxis_title={'categoryorder':'total descending'},
        showlegend=False
    )
       
    return fig