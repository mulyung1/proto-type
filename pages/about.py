from dash import html, register_page
import dash_bootstrap_components as dbc

#register the page
register_page(
    __name__,
    name='About',
    path='/about'
)

#layout of page
def layout():
    return dbc.Container([
        dbc.Row([
            html.Div(
                html.P("This project is funded by the International Fund for Agricultural Development (IFAD) and led by ICRAF in close collaboration with national partners (country projects) in Kenya. The main objective of the project was to develop an EO-assisted platform where IFAD and other stakeholders can access information and maps for key indicators of ecosystem health. The indicator sets included on the platform are directly relevant to IFAD's Results and Impact Management System (RIMS), with particular focus on indicators of soil and land health relevant for the sustainability of land management practices.",
                style={
                    #"border-left": "5px solid #ccc",
                    "margin-left": "1.5em 10px",
                    "padding": "0.5em 10px",
                    "background-color": "#8fbc8f",
                    'fontSize':15,
                    'boxShadow': '0 4px 8px rgba(1, 0.9, 0.8, 0.9)'
                }
                )
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.P("State-of-the-art EO data and analytical procedures are presented through user-friendly dashboards for data interaction and exploration. The use of open source technologies is a critical component of the project as this ensures transparency and sustainable impact beyond the grant period. It further allows for further development of the system by the open-source community beyond the duration of the project, for example through cloning and applications of the developed system in other contexts where relevant.",
                    style={
                    #"border-left": "5px solid #ccc",
                    "margin-left": "1.5em 10px",
                    "padding": "0.5em 10px",
                    "background-color": "#8fbc8f",
                    'fontSize':15,
                    'boxShadow': '0 4px 8px rgba(1, 0.9, 0.8, 0.9)'}
                    )
                )
            ),
            dbc.Col(
                html.Div(
                    html.P("The combination of EO data and ground observations and data analytics provides a framework for operationalizing assessments and monitoring of ecosystem health. The Ecosystem Health Surveillance System (EcoHSS) was developed at ICRAF in response to the need for systematic assessments of ecosystem health globally, building “gold standard” biophysical datasets for the key indicators mentioned above. The development of the EcoHSS has come about through a number of different projects, including IFAD ASAP projects in about 15 countries in Africa, where the approach has been tested and deployed in project planning, for example.",
                    style={
                    #"border-left": "5px solid #ccc",
                    "margin-left": "1.5em 10px",
                    "padding": "0.5em 10px",
                    "background-color": "#8fbc8f",
                    'fontSize':15,
                    'boxShadow': '0 4px 8px rgba(1, 0.9, 0.8, 0.9)'}
                    )
                )
            )
        ]),
        dbc.Row([
            html.Div([
                html.H2('Conceptual framework'),
                html.P("The conceptual framework behind the project is shown below. It builds on the Land Degradation Surveillance Framework (LDSF) for biophysical (ecological) assessment and monitoring of ecosystem health using from field surveys and earth observation. We combine these ecological assessments with data from socio-economic surveys, including household surveys, where available.",
                       style={'font-size':15}
                ),
            ],style={
                "border-left": "5px solid #ccc",
                'width':300,
                }),
            html.Div([
                html.Img(src='assets/conceptual_framework.png', style={'width': '100%', 'height': 'auto'})
            ],
            style={
                'height':800,}
            )
        ])
    ], fluid=True)