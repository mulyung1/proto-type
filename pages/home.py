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
        html.H3('Let us explore the world via indicators over a period of 43 years since 1957', className='main-heading'),
        dbc.Row([
            dbc.Col([
                html.Blockquote([
                    html.Strong('Why Python Dash?'),
                    html.Br(),
                    "Dash, a powerful framework for building interactive web applications with Python. Dash simplifies the process of building dashboards by allowing developers to use Python, a language already familiar to many in the data science and analytics community. Dash applications are easy to deploy, scalable, and can be rendered in any web browser, making them accessible across different platforms. Additionally, Dash’s component-based architecture, combined with its support for callbacks, ensures that applications are dynamic and responsive to user interactions."
                ], className='blockquote')
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P('Coming soon', className='coming-soon')
                ], className='coming-soon-div'),
                dcc.RadioItems(
                    options=[
                        {'label': 'Population', 'value': 'pop'},
                        {'label': 'Life Expectancy', 'value': 'lifeExp'},
                        {'label': 'GDP Per Capita', 'value': 'gdpPercap'}
                    ],
                    value='lifeExp',
                    inline=True,
                    id='batons',
                    labelStyle={'fontSize': 15, 'color': 'LightGreen'}
                ),
                dcc.Graph(id='graf')
            ], width=6),
            dbc.Col([
                html.Div([
                    html.H3('Choropleth Map', className='map-heading'),
                    html.Iframe(id='map', className='map-iframe')
                ], className='map-div')
            ])
        ])
    ], fluid=True, className='container')

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
