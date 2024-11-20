import pandas as pd
import plotly_express as px
from dash import Dash,html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import adam, alex, jonte, tobbe

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])                                        # Initialize app

options_list = list() 
options_list += [ {"label":key, "value":key} for key in adam.select.keys() ] 
options_list += [ {"label":key, "value":key} for key in alex.select.keys() ] 
options_list += [ {"label":key, "value":key} for key in jonte.select.keys() ] 
options_list += [ {"label":key, "value":key} for key in tobbe.select.keys() ] 

app.layout = [                                              # layout-design
    html.Div(children = "Project OS", style={"text-align": "center","font-size": "40px", "font-weight": "bold", "color": "#4CAF50"}),
    html.Hr(),
    dcc.Dropdown(                                                                       # Dropdown on dash, with labels and values.
    id="Sport dropdown",
    options = options_list,
    #options = [
    #        {"label": "Weightlifting", "value": "Weightlifting"},
    #        {"label": "Archery", "value": "Archery"},
    #        {"label": "Gymnastics", "value": "Gymnastics"},
    #        {"label": "Age distribution with medals", "value": "Age distribution"}
    #        ],

    placeholder="Select a sport", 
    style={"width": "45%", "margin": "auto", "padding": "10px"},     # Gives dropdown a "default text"
    ),
    dcc.Graph( id="Medal chart", )    
]

@app.callback(                                                                  # Gives the dashapp input and output, user input linked with app output.
    Output("Medal chart", "figure"),
    Input("Sport dropdown", "value")
)
def medal_chart(selection_of_sport):

    if not selection_of_sport:                                                  # if no choice - show empty graph.
        return {}
    
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
    return select[selection_of_sport]



if __name__ == "__main__":                                  # Runs the app
    app.run(debug=True)