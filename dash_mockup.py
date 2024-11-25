# Används inte.. Tabort?
# [
import pandas as pd
import plotly.express as px
# ] 
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import charts


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


options_list = [{"label": key, "value": key} for key in charts.select.keys()]

app.layout = html.Div(
    style={
        'backgroundColor': '#FBE9D1',
        'height': '100vh',
        'display': 'flex',
        'flexDirection': 'column',
    },
    children=[
        html.Div(
            children=[
                html.Div(
                    "Project OS",
                    style={
                        "text-align": "center",
                        "font-size": "40px",
                        "font-weight": "bold",
                        "color": "#444339",
                    }
                ),
                html.Hr(),
                dcc.Dropdown(
                    id="Sport-dropdown",
                    options=options_list,
                    placeholder="Select a sport",
                    style={
                        "width": "20vw",
                        "margin": "auto",
                        "padding": "0px",
                        'border': '1px solid #444339',
                        'border-radius': '4px'
                    },
                    value="Hungary Overview"
                ),
                html.Div(className='dbc',
                         style={"display": "flex",
                                "justifyContent": "center", "margin-top": "20px"},
                         children=[
                             dbc.Button(
                                 'Previous', id='prev-button', n_clicks=0, style={"backgroundColor": "#EFE1BA", "color": "#444339", 'border': '2px solid #444339',
                                                                                  'border-radius': '6px', }),
                             dbc.Button('Next', id='next-button',
                                        n_clicks=0, style={"margin-left": "10px", "backgroundColor": "#EFE1BA", "color": "#444339", 'border': '2px solid #444339',
                                                           'border-radius': '6px', }),
                         ]
                         ),
            ],
            style={
                'flex': '0 0 auto',
                'padding': '20px',
                'backgroundColor': '#F1F0EB'
            }
        ),
        dcc.Store(id="chart-index", data=0),
        html.Div(
            id="Div chart",
            children={},
            style={
                'flex': '1 1 auto',
                'padding': '20px',
                'backgroundColor': '#F1F0EB'
            }
        )
    ]
)


@app.callback(
    [Output("Div chart", "children"),
     Output("Sport-dropdown", "value")],
    Input("chart-index", "data"),
    State("Sport-dropdown", "value")
)
def update_chart(chart_index, dropdown_value):
    if not dropdown_value:
        dropdown_value = "Hungary Overview"

    select = charts.select
    keys = list(select.keys())

    chart_index = chart_index % len(keys)
    chart_key = keys[chart_index]

    return select.get(chart_key, html.Div("No chart available")), chart_key


@app.callback(
    Output("chart-index", "data"),
    [Input("prev-button", "n_clicks"), Input("next-button", "n_clicks")],
    State("chart-index", "data")
)
def update_index(prev_clicks, next_clicks, current_index):
    return current_index + (next_clicks - prev_clicks)


if __name__ == "__main__":
    app.run(debug=True)
