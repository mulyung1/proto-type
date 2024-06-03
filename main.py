import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from sidebar import create_sidebar

# CSS styles
FA621 = 'https://use.fontawesome.com/releases/v6.2.1/css/all.css'
appstyle = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
SIDEBAR = create_sidebar()
APP_TITLE = 'MGC SOFWARE SOLUTIONS'

# Initialize the app
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[FA621, appstyle, dbc.themes.FLATLY],  # Choose one theme
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],  # Responsive meta tag
    title=APP_TITLE,
    use_pages=True,
)
server=app.server

# Define the app layout
app.layout = dcc.Loading(
    id='loading_content',
    children=[
        dbc.Row([
            dbc.Col(
                [SIDEBAR],  # Place SIDEBAR here
                # Adjust sidebar column for different screen sizes
                xs=12, #extra small screen
                sm=12, #small screen
                md=3, #medium screen
                lg=3, #large screen
                xl=2, #extra large screen
                xxl=2  # extra extra large screen
            ),
            dbc.Col([
                html.Div(
                    dash.page_container,
                    style={
                        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',  # Subtle shadow for better appearance
                        'padding': '20px',
                        'background-color': '#add8e6',
                        'border-radius': '6px',
                        'margin-top': '20px',
                        'margin-left': '15px',
                        'margin-right': '15px',  # Added right margin for consistent spacing
                        'width': '100%',  # Set width to 100% for responsive design
                        'height': 'calc(100vh - 60px)',  # Adjust height dynamically
                        'overflowY': 'auto',  # Enable vertical scrolling if needed
                        'background-image': "url('assets/mlima.jpg')",
                        'background-size': 'cover',
                        'background-repeat': 'no-repeat',
                        'background-position': 'center'
                    }
                )
            ], xs=12, sm=12, md=9, lg=9, xl=10, xxl=10)  # Adjust main content column for different screen sizes
        ])
    ]
)

# Run the app
if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=8888)
