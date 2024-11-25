from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import charts

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


options_list = [{"label": key, "value": key} for key in charts.select.keys()]

default_chart = "Hungary Overview"
default_index = list(charts.select.keys()).index(default_chart)


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
                    value=default_chart
                ),
                html.Div(
                    className='dbc',
                    style={"display": "flex",
                           "justifyContent": "center", "margin-top": "20px"},
                    children=[
                        dbc.Button(
                            'Previous', id='prev-button', n_clicks=0,
                            style={
                                "backgroundColor": "#EFE1BA",
                                "color": "#444339",
                                'border': '2px solid #444339',
                                'border-radius': '6px'
                            }
                        ),
                        dbc.Button(
                            'Next', id='next-button', n_clicks=0,
                            style={
                                "margin-left": "10px",
                                "backgroundColor": "#EFE1BA",
                                "color": "#444339",
                                'border': '2px solid #444339',
                                'border-radius': '6px'
                            }
                        ),
                    ]
                ),
            ],
            style={
                'flex': '0 0 auto',
                'padding': '20px',
                'backgroundColor': '#F1F0EB'
            }
        ),

        dcc.Store(id="chart-index", data=default_index),
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
     Output("Sport-dropdown", "value"),
     Output("chart-index", "data")],
    [Input("prev-button", "n_clicks"),
     Input("next-button", "n_clicks"),
     Input("Sport-dropdown", "value")],
    State("chart-index", "data")
)
def update_chart(prev_clicks, next_clicks, dropdown_value, current_index):
    select = charts.select
    keys = list(select.keys())

    ctx = callback_context

    if ctx.triggered and ctx.triggered[0]["prop_id"] == "Sport-dropdown.value":

        if dropdown_value in keys:
            current_index = keys.index(dropdown_value)
    elif ctx.triggered and "prev-button" in ctx.triggered[0]["prop_id"]:

        current_index = (current_index - 1) % len(keys)
    elif ctx.triggered and "next-button" in ctx.triggered[0]["prop_id"]:

        current_index = (current_index + 1) % len(keys)

    chart_key = keys[current_index]
    chart = select.get(chart_key, html.Div("No chart available"))

    return chart, chart_key, current_index


if __name__ == "__main__":
    app.run(debug=True)
