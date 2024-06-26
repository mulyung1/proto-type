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
        html.Div(html.P('Coming soon'))
    ], fluid=True)