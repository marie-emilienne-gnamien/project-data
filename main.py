#
# Imports
#
import folium
import plotly.express as px
import dash
from dash import html, dcc, Dash, ctx
from dash.dependencies import Input,Output
import mapAndGraphs as mG

years = mG.data['year'].unique()

if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    fig = px.scatter(mG.data[mG.year], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country") # (4)


    app.layout = html.Div(children=[

                            html.H1(children=f'Study of Natural Disaster Events ({mG.year})',
                                        style={'textAlign': 'center', 'color': "#47793B"},
                                        id="title"), # (5)

                            dcc.Graph(
                                id='carte1',
                                figure=mG.carte
                            ), # (6)

                            html.Div(children=f'''
                                The map above shows various Natural Disasters which happened in the world during {mG.year}. Each country displayed has its own data and
                                colour.
                                Mouse over for details.\n
                            ''',
                            id="description_carte"), # (7)

                            html.Label('Select Year:'),
                                dcc.Slider(
                                    step=None,
                                    id="year-slider",
                                    marks={str(year) : str(year) for year in years},
                                    value=2024,
                                )
                                # dcc.Interval(id="interval",
                                #              interval=1*1000, # in milliseconds
                                #              n_intervals=0,
                                #              disabled=False),

                            # html.Button('Play', id='play-button', n_clicks=0),
                            # html.Button('Stop', id='stop-button', n_clicks=0)
                        ]
    )

    l = [Output(component_id='graph1', component_property='figure'),Output(component_id="title",component_property="children"),Output(component_id="description",component_property="children")]
    @app.callback(l, # (1)
    [Input(component_id='year-slider', component_property='value')] # (2)
    )

    def update_figure(selected_year): # (3)
        description = f'''
                            The graph above shows relationship between life expectancy and
                            GDP per capita for year {selected_year}. Each continent data has its own
                            colour and symbol size is proportionnal to country population.
                            Mouse over for details.\n
                        '''
        return px.scatter(data[selected_year], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country",
                        labels={"continent":"Continent"}
                        ),f'Life expectancy vs GDP per capita ({selected_year})',description
    

    @app.callback(Output('year-slider','value'),
                  [Input('interval','n_intervals')])
    def on_tick(n_intervals):
        if n_intervals is None: return 0
        return years[(n_intervals+1) % len(years)]
    
    @app.callback(Output('interval', 'disabled'),
                  [Input('stop-button','n_clicks'),Input('play-button','n_clicks')])
    def on_off_animation(play,stop):
        if 'stop-button' == ctx.triggered_id:
            return True
        if 'play-button' == ctx.triggered_id:
            return False
        
    #
    # RUN APP
    #

    app.run(debug=True) # (8)


