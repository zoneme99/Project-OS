import pandas as pd
import plotly_express as px
from dash import html, dcc, dash_table

# Create your charts here 
df = pd.read_csv("Data/athlete_events.csv") 

def Gold_Fencing_Men():
    othermen = len(df[(df['Sex'] == 'M') & (df['Sport'] == 'Fencing') & (df['NOC'] != 'HUN') & (df['Medal'] == 'Gold')])
    hungarymen = len(df[(df['Sex'] == 'M') & (df['Sport'] == 'Fencing') & (df['NOC'] == 'HUN') & (df['Medal'] == 'Gold')])
    return [othermen, hungarymen]

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
        "Gold Fencing Men": dcc.Graph( figure=px.pie(values=Gold_Fencing_Men(), names=["Other Men", "Hungarian Men"], title="Gold medals in Fencing"), template="slate" ),
}