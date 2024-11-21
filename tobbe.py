import pandas as pd
import plotly_express as px
from dash import html, dcc, dash_table

# Create your charts here 
df = pd.read_csv("Data/athlete_events.csv") 

def select_sport(selection_of_sport):
    chosen_sport = (df["Sport"] == selection_of_sport) & (df["Medal"].notna())
    medals_by_country = (df[chosen_sport].groupby("NOC")[["Medal"]].count().sort_values(by="Medal",ascending=False).reset_index()) # groups by NOC and counts number of medals, sort values and then resets index.
    return medals_by_country

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
        "Weightlifting": dcc.Graph( figure=px.bar(
            select_sport("Weightlifting"),
            x="NOC",
            y="Medal",
            color="NOC",
            title= f"Medal overview in Weightlifting"
         )),
        "Archery": dcc.Graph( figure=px.bar(
            select_sport("Archery"),
            x="NOC",
            y="Medal",
            color="NOC",
            title= f"Medal overview in Archery"
         )),
        "Gymnastics":dcc.Graph( figure= px.bar(
            select_sport("Gymnastics"),
            x="NOC",
            y="Medal",
            color="NOC",
            title= f"Medal overview in Gymnastics"
         )),
}