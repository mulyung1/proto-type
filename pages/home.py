
from dash import Dash, html, register_page, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import folium
import requests
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
from cache_config import cache


register_page(
    __name__,
    name='MGC SOFT SOLNS',
    #top_nav=True,
    path='/'
)

# Load the CSV data
dff = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = dff[dff['continent'].isin(['Africa', 'Asia', 'Europe', 'Americas', 'Oceania'])]


#define the app layout
def layout():
    return dbc.Container([
        dcc.Store(id='signal'),
        html.H3('Data and evidence to strengthen baseline assessments, inform interventions and monitor impacts across landscapes', style={'font-weight':'bold'}),
        dbc.Row([
            dbc.Col([
                html.Blockquote([
                    html.Strong('Why this dashboard?'),
                    html.Br(),
                    "This dashboard was developed in response to the ongoing challenge of increasing the impact of development projects through better-informed project design, by using improved baseline assessments, and through results-based management on the ground.",
                ],style={
                    'width':200,
                    "border-left": "5px solid #ccc",
                    "margin": "1.5em 10px",
                    "padding": "0.5em 10px",
                    "background-color": "#8fbc8f",
                    'fontSize':15,
                    'boxShadow': '0 4px 8px rgba(1, 0.9, 0.8, 0.9)'
                    }
                ),
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P('We use robust, readily measurable, and scientifically rigorous, indicators to assess landscape “ecosystem health” in terms of both biophysical indicators (e.g. soil erosion, soil fertility and vegetation dynamics), and socio-economic indicators. Here, the recent revolution in quality and accessibility of Earth Observation (EO) data presents a major opportunity for smallholder farmers and to development projects. Combining EO data of landscape-level ecosystem health, with field level information on production and household income will result in a leap forward in terms of impact.',
                        style={'margin-left': 20, 'fontSize':15}
                    )
                ], style={
                    'width': '100%',
                    'backgroundColor': '#8fbc8f',
                    'boxShadow': '0 4px 8px rgba(1, 0.9, 0.8, 0.9)'
                }),
                dcc.RadioItems(
                    options=[
                        {'label':'Population', 'value':'pop'},
                        {'label':'Life Expectancy', 'value':'lifeExp'},
                        {'label':'Gdp Per Cap', 'value':'gdpPercap'},
                    ],
                    value='lifeExp',
                    inline=True,
                    id='batons',
                    labelStyle={'fontSize':15,'color':'LightGreen'}
                ),
                dcc.Graph(id='graf'),
            ], width=6),
            dbc.Col([
                html.Div([
                    html.H3('Choropleth Map', style={'textAlign':'center'}),
                    html.Iframe(id='map', width='100%', height='100%')], 
                    style={
                        'width': '100%', 
                        'height': '57.5%', 
                        'margin-bottom':40,
                    }
                ),
                html.Br(),
                html.Div([
                    html.P('Poor rural households are in the front line of climate change impacts and face a series of interconnected natural resource management challenges. The ecosystems and biodiversity on which they rely are increasingly degraded; their access to suitable agricultural land is declining in quantity and quality. The limited capacity of rural people to deal with these challenges is a major hurdle for them to escape from extreme poverty. Evidence-based decision making is critically important if we are to transform the agricultural sector in developing countries, including actionable data and evidence for smallholder farmers to make decisions about their own management interventions.',
                        style={'margin-left': 20, 'fontSize':15}
                    )
                ], style={
                    'width': '100%',
                    'backgroundColor': '#8fbc8f',
                    'boxShadow': '0 4px 8px rgba(1, 0.9, 0.8, 0.9)'
                })
            ], width=6)
        ])   
    ], fluid=True, style={
        'height': 'calc(120vh - 60px)',
        'width': '100%',
        'borderRadius': 6}
    )


@cache.memoize()
def global_store(selected_value):
    print(f'Computing value with {selected_value}')
    filtered_data = df[['country', 'continent', selected_value]]
    geojson_data = requests.get(
        'https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json'
    ).json()
    return filtered_data, geojson_data

def create_choropleth_map(data, geojson_data, selected_value):
    m = folium.Map(
        location=[42.45736003202464, 15.962058394747377],
        zoom_start=1
    )
    folium.TileLayer('openstreetmap').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)

    folium.Choropleth(
        geo_data=geojson_data,
        name="choropleth",
        data=data,
        columns=["country", selected_value],
        key_on="feature.properties.name",
        fill_color="YlGn",
        fill_opacity=1,
        line_opacity=0.2,
        nan_fill_color="grey",
        nan_fill_opacity=0.2,
        legend_name=f"{selected_value} Rate",
        highlight=True,
    ).add_to(m)
    folium.LayerControl().add_to(m)

    map_path = 'map.html'
    m.save(map_path)
    with open(map_path, 'r') as f:
        map_html = f.read()
    return map_html


# Callback to store the selected value, data, and geojson_data in dcc.Store
@callback(
    Output('signal', 'data'),
    Input('batons', 'value')
)
def update_signal(selected_value):
    if selected_value is None:
        raise PreventUpdate

    filtered_data, geojson_data = global_store(selected_value)

    return {'selected_value': selected_value, 'filtered_data': filtered_data.to_dict('records'), 'geojson_data': geojson_data}

# Callback to update the graph
@callback(
    Output('graf', 'figure'),
    Input('signal', 'data')
)
def update_graph(signal_data):
    if signal_data is None:
        raise PreventUpdate

    filtered_data = pd.DataFrame(signal_data['filtered_data'])
    selected_value = signal_data['selected_value']

    fig = px.histogram(
        filtered_data, 
        x='continent',
        y=selected_value, 
        histfunc='avg', 
        height=420,
        title=f'Histogram for {selected_value}'
    )
    return fig

# Callback to update the map
@callback(
    Output('map', 'srcDoc'),
    Input('signal', 'data')
)
def update_map(signal_data):
    if signal_data is None:
        raise PreventUpdate

    filtered_data = pd.DataFrame(signal_data['filtered_data'])
    geojson_data = signal_data['geojson_data']
    selected_value = signal_data['selected_value']
    map_html = create_choropleth_map(filtered_data, geojson_data, selected_value)
    return map_html
