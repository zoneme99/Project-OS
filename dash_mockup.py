import pandas as pd
import plotly_express as px
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import adam
import alex
import jonte
import tobbe

# Initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# Imports the select dictionary from each persons file and
# extrackts the key and coverts it a lable value pair that
# the drop down menu can use
options_list = list()
options_list += [{"label": key, "value": key} for key in adam.select.keys()]
options_list += [{"label": key, "value": key} for key in alex.select.keys()]
options_list += [{"label": key, "value": key} for key in jonte.select.keys()]
options_list += [{"label": key, "value": key} for key in tobbe.select.keys()]

app.layout = dbc.Container(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    "Project OS"
                ),
                dbc.Col(
                    dcc.Dropdown(
                    id="Sport-dropdown",
                    options=options_list,
                    placeholder="Select a sport",
                    value="Medal Distribution For Hungary",
                    className="dbc"
                )
                )

            ])
        ,
        dbc.Row(
            id="Div chart",
            children={},
            className="dbc"

        )
    ]
    , fluid=True,
    className="dbc"
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
    select = dict()
    select.update(adam.select)
    select.update(alex.select)
    select.update(jonte.select)
    select.update(tobbe.select)
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
