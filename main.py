
import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from sidebar import create_sidebar
from cache_config import cache
#import dash_loading_spinners as dls

# CSS styles
FA621 = 'https://use.fontawesome.com/releases/v6.2.1/css/all.css'
appstyle = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
SIDEBAR = create_sidebar()
APP_TITLE = 'MGC SOFTWARE SOLUTIONS'

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
cache.init_app(server)

# Define the app layout
app.layout = dcc.Loading(
    id='loading_content',
    type='dot',
    overlay_style={'visibility':'visible'},
    color='#8fbc8f',
    children=[
        dbc.Row([
            dbc.Col(
                [SIDEBAR],  # Place SIDEBAR here
                className='sidebar-col'
            ),
            dbc.Col([
                html.Div(
                    dash.page_container,
                    className='landingpage'
                )
            ], xs=12, sm=12, md=9, lg=9, xl=10, xxl=10)  # Adjust main content column for different screen sizes
        ])
    ]
)

# Run the app
if __name__ == '__main__':
    app.run()
#debug=True, threaded=True, port=8888