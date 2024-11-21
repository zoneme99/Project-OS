import pandas as pd
import plotly_express as px
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

# Create your charts here 
df = pd.read_csv("Data/athlete_events.csv") 

def select_sport(selection_of_sport):
    chosen_sport = (df["Sport"] == selection_of_sport) & (df["Medal"].notna())
    medals_by_country = (df[chosen_sport].groupby("NOC")[["Medal"]].count().sort_values(by="Medal",ascending=False).reset_index()) # groups by NOC and counts number of medals, sort values and then resets index.
    return medals_by_country

df_info = pd.DataFrame() 
df_info["Hosts"] = "Athens,France,USA,UK,Sweden".split(",")
df_info["Year"] = "1896,1900,1904,1908,1912".split(",")
# Add your completed charts to the select dictionary
# select={ 
#   "chart_name_a": dcc.Graph( figure=px.bar(    )), 
#   "chart_name_b": dcc.Graph( figure=px.line(   )),
# }
# the dcc.Graph is the element used by app.layout = [] to display graphs
# the figure= contains the plotly_express chart
# check the tobbe.py file for further references
# NOTE You should be able to add any tipe of object like a string, dash_table or another div
select={
        "Sailing": dcc.Graph( figure=px.bar(
            select_sport("Sailing"),
            x="NOC",
            y="Medal",
            color="NOC",
            title= f"Medal overview in Sailing"
         )),
        "Canoeing": dcc.Graph( figure=px.bar(
            select_sport("Canoeing"),
            x="NOC",
            y="Medal",
            color="NOC",
            title= f"Medal overview in Canoeing"
         )),
         #Project-OS\olympic_flag_2.png
         #Project-OS\olympic_flag_2.png
         
         "h1_test": html.H1(children="Great Scott"),
         "div_test": html.Div(children=[
             html.Img( style={ "width":"400px", "height":"247px", },  src="https://upload.wikimedia.org/wikipedia/commons/a/a7/Olympic_flag.svg" ),
             dbc.Table.from_dataframe(df_info)
            ]),

}