from dash import Dash, dcc, html, callback, Output, Input, dash_table, register_page
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Connect to the data
df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

# Body of the website
markdown_text = '''
### Is there a relationship between the contribution of the industry sector to GDP (value added %) and CO2 emissions per capita in an economy??

Are the two indicators correlated, i.e., does the occurrence of one (x) influence the occurrence of another (y)??

   >_Select the variable for X axis from the LHS input panels_

   >_Select the variable for Y axis from the RHS input panels_

#### Time Series
   > What do the time-series graphs tell us the trend is??
   
   > Update the time series graphs to the right when you hover over the points in the scatter plot
'''


# Register the page
register_page(
    __name__,
    name='comparative',
    path='/comparative'
)

# Define the page layout
def layout():
    return dbc.Container([
        dbc.Row([
            html.H1('Does X affect Y?'),
            html.Hr(),
            dcc.Markdown(children=markdown_text, style={'fontSize':15})
        ]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            df['Indicator Name'].unique(),
                            'Industry, value added (% of GDP)',
                            id='independent_var',
                            # optionHeight=40,
                            className='customDropdown'
                        ),
                        dcc.RadioItems(
                            ['Linear', 'Log'],
                            'Log',
                            inline=True,
                            id='dt_type_x',
                            labelStyle={'display': 'inline-block', 'fontSize':15}
                        )
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            df['Indicator Name'].unique(),
                            'CO2 emissions (metric tons per capita)',
                            id='dependent_var',
                            # optionHeight=40,
                            className='customDropdown',
                        ),
                        dcc.RadioItems(
                            ['Linear', 'Log'],
                            'Log',
                            inline=True,
                            id='dt_type_y',
                            labelStyle={'display': 'inline-block','fontSize':15}
                        )
                    ],
                    width=6
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='graf1', hoverData={'points': [{'customdata': 'Kenya'}]})
                    ], 
                    width=6
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='xt_graf'),
                        dcc.Graph(id='yt_graf')
                    ], 
                    width=6
                )
            ]
        ),
        dbc.Row(
            [
                dcc.Slider(
                    df['Year'].min(),
                    df['Year'].max(),
                    step=None,
                    value=1977,
                    id='sliida',
                    marks={str(year): str(year) for year in df['Year'].unique()},
                    tooltip={"placement": "bottom", "always_visible": True, "template": "Year: {value}"},
                )
            ]
        ),
        dbc.Row(
            [
                html.H2('Data Used', style={'margin-top':'50px'}),
                html.Hr(),
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    page_size=11,
                    style_table={'overflowX': 'auto'},
                    style_data={'backgroundColor': 'rgba(58, 123, 151, 0.5)','color': 'white', 'fontSize':15},
                    style_header={'backgroundColor': 'rgb(199, 11, 105)','color': 'white', 'fontWeight':'bold','fontSize':15},
                    style_cell={ 'border': '1px solid white' },
                )
            ]
        )
    ], fluid=True)

# Callback decorators and time series creation function
# Callback decorator + function to update scatter plot - 'Graf'
@callback(
    Output('graf1', 'figure'),
    Input('independent_var', 'value'),
    Input('dependent_var', 'value'),
    Input('dt_type_x', 'value'),
    Input('dt_type_y', 'value'),
    Input('sliida', 'value')
)
def updateGraf(indep_var, dep_var, type_x, type_y, time):
    dff = df[df['Year'] == time]
    fig = px.scatter(
        x=dff[dff['Indicator Name'] == indep_var]['Value'],
        y=dff[dff['Indicator Name'] == dep_var]['Value'],
        hover_name=dff[dff['Indicator Name'] == dep_var]['Country Name']
    )
    fig.update_traces(customdata=dff[dff['Indicator Name'] == dep_var]['Country Name'])
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    fig.update_xaxes(title=indep_var, type='log' if type_x == 'Log' else 'linear')
    fig.update_yaxes(title=dep_var, type='log' if type_y == 'Log' else 'linear')
    return fig

# Function that creates the time series
def create_time_series(dff, axis_type, title):
    fig = px.scatter(dff, x='Year', y='Value')
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(type='log' if axis_type == 'Log' else 'linear')
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)
    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    return fig

# Callback decorators + functions that update the time series graphs
# 1 (decorator) - updates the x_Time_series graph
@callback(
    Output('xt_graf', 'figure'),
    Input('graf1', 'hoverData'),
    Input('independent_var', 'value'),
    Input('dt_type_x', 'value')
)
def updateXTseries(hoverData, indep_var, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == indep_var]
    title = '<b>{}</b><br>{}'.format(country_name, indep_var)
    return create_time_series(dff, axis_type, title)

# 2 (decorator) - updates the y_Time_series graph
@callback(
    Output('yt_graf', 'figure'),
    Input('graf1', 'hoverData'),
    Input('dependent_var', 'value'),
    Input('dt_type_y', 'value')
)
def updateYTseries(hoverData, dep_var, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == dep_var]
    return create_time_series(dff, axis_type, dep_var)
