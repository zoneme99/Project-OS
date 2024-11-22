import pandas as pd
import plotly_express as px
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import adam
import alex
import jonte
import tobbe
import charts as charts

# Initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Imports the select dictionary from each persons file and
# extrackts the key and coverts it a lable value pair that
# the drop down menu can use
options_list = list()
options_list += [{"label": key, "value": key} for key in charts.select.keys()]
# options_list += [{"label": key, "value": key} for key in adam.select.keys()]
# options_list += [{"label": key, "value": key} for key in alex.select.keys()]
# options_list += [{"label": key, "value": key} for key in jonte.select.keys()]
# options_list += [{"label": key, "value": key} for key in tobbe.select.keys()]

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
                        "padding": "0px"
                    },
                    value="Medal Distribution For Hungary"
                ),

            ],
            style={
                'flex': '0 0 auto',
                'padding': '20px',
                'backgroundColor': '#F1F0EB'
            }
        ),
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


@app.callback(                                                                  # Gives the dashapp input and output, user input linked with app output.
    Output("Div chart", "children"),
    Input("Sport-dropdown", "value")
)
def medal_chart(selection_of_sport):

    if not selection_of_sport:
        # if no choice - show empty graph.
        return {}
        # return px.bar(title="")

    # Imports the select dictionary that contains the
    # charts from each persons file
    select = charts.select
    # select.update(adam.select)
    # select.update(alex.select)
    # select.update(jonte.select)
    # select.update(tobbe.select)
    """
    select={
        "Weightlifting": px.bar(
            select_sport("Weightlifting"),
            x="NOC",
            y="Medal",
            color="NOC",
            title= f"Medal overview in Weightlifting"
         ),
        "Archery": px.bar(
            select_sport("Archery"),
            x="NOC",
            y="Medal",
            color="NOC",
            title= f"Medal overview in Archery"
         ),
    """
    # return select[selection_of_sport]
    return (select[selection_of_sport],)


if __name__ == "__main__":                                  # Runs the app
    app.run(debug=True)
