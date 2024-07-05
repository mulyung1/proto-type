'''
This app
-> multipage dash app
-> creates a collapsible, responsive sidebar with dbc
-> custom css has media querries 

small screen?
-> sidebar moves to the top
-> a collapse element hides the links
callback?
-> toggles the collapse in the small screen 
custom css? 
-> hides the toggle
-> forces collapse to stay open on a LARGE SCREEN

dcc.Location
-> tracks current location

page_content?
-> rendered via the das.page_container

active prop?
-> set automatically according to the current pathname

'''


import dash
from dash import Dash, dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
from cache_config import cache
#import dash_loading_spinners as dls

# CSS styles
FA621 = 'https://use.fontawesome.com/releases/v6.2.1/css/all.css'
appstyle = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
APP_TITLE = 'World View Dashboard'

# Initialize the app
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[FA621, appstyle, dbc.themes.QUARTZ],  # Choose one theme
    #metatags ensure content is scaled correctly in different screen sizes
    # for more info see: https://www.w3schools.com/css/css_rwd_viewport.asp
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],  # Responsive meta tag
    title=APP_TITLE,
    use_pages=True,
)
server=app.server
cache.init_app(server)

#dbc Row and Col components construct the sidebar header
#i.e. a title, a toggle(hidden on large screens)
navbarHeader=dbc.Row(
    [
        dbc.Col(html.H3('Historical World', className='display-3')),
        dbc.Col(
            [
                html.Button(
                    #style the toggle using Bootstrap navbar-toggle classes
                    html.Span(className='navbar-toggler-icon'),
                    className='navbar-toggler',
                    #set color as navbar-togler classes don't
                    style={
                        'fontSize':20,
                    },
                    id='navbar_toggle'
                ),
                html.Button(
                    #style the toggle using Bootstrap navbar-toggle classes
                    html.Span(className='navbar-toggler-icon'),
                    className='navbar-toggler',
                    #set color as navbar-togler classes don't
                    style={
                        'fontSize':20,
                    },
                    id='top_toggle'
                ),
            ],
            #column with toggle is as wide as 
            #the toggle, and toggle is right aligned
            width='auto',
            align='center'
        )
    ]
)

navbar=html.Div(
    [
        navbarHeader,
        #wrap the html.Hr + a short blurb
        #in a div element that can be hidden on a small screen
        html.Div(
            [
                html.Hr(),
                html.P('A Python based data app developed '
                'by MGC SoftWare Solutions.',
                className='lead', style={'fontSize':15})
            ],
            id='blurb'
        ),
        #collapse component animates hiding/revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink([html.I(className='fa-solid fa-house'), 'Home'],  href='/', active='exact', style={'fontSize':15}),
                    dbc.NavLink([html.I(className='fa-solid fa-folder-open'), 'Project Details'], href='/about', active='exact', style={'fontSize':15}),
                    dbc.NavLink([html.I(className='fa-brands fa-github'),'Code'], href='https://github.com/mulyung1', active='exact', target='_blank_', style={'fontSize':15}),
                ],
                vertical=True,
                pills=True
            ),
            id='collapse'
        )
    ], 
    id='navbar'
)

content=html.Div(dash.page_container, id='page_content')


app.layout=dcc.Loading(
    id='loading_content',
    type='dot',
    overlay_style={'visibility':'visible'},
    color='#8fbc8f',
    children=[
        html.Div(
            [
                dcc.Location(id='url'),
                navbar,
                content     
            ]       
        )
    ]
)

@callback(
    Output('navbar', 'className'),
    [Input('navbar_toggle', 'n_clicks')],
    [State('navbar', 'className')]
)
def toggle_classname(n, className):
    if n and className =='':
        return 'collapsed'
    return ''

@callback(
    Output('collapse', 'is_open'),
    [Input('top_toggle', 'n_clicks')],
    [State('collapse', 'is_open')]
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Run the app
if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=8888)
#debug=True, threaded=True, port=8888