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
def age_distribution(chosen_sports):
    """
    Generates a boxplot for the age distribution of athletes across the given sports.
    """
    filt_df = df[df["Sport"].isin(chosen_sports)]
    # Color map for medals
    color_map = {
        "Gold": "#FFD700",   # Gold color hexadecimal
        "Silver": "#C0C0C0", # Silver color hexadecimal
        "Bronze": "#CD7F32"  # Bronze color hexadecimal
    }
    # Create boxplot
    fig = px.box(filt_df, 
                 x="Sport", 
                 y="Age", 
                 color="Medal", 
                 title="Age distribution in Fencing, Water Polo, and Gymnastics",
                 color_discrete_map=color_map,
                 template="plotly")
    return fig
    


select={
        "Age distribution": dcc.Graph( figure= age_distribution(["Fencing","Water Polo", "Gymnastics"]
        )), 
        



        "Hungary": html.Div(style={"display":"flex", "align-items":"center", "gap":"20px"},
            children=[
            
            html.Img( style={ "width":"400px", "height":"247px", "border":"3px solid black", "display":"block"},  src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Flag_of_Hungary.svg" ),
            html.Img( style={ "width":"400px", "height":"247px", "border":"3px solid black", "display":"block"},  src="https://upload.wikimedia.org/wikipedia/commons/a/a7/Olympic_flag.svg" ),
            
            html.Div(children=[
                html.H3("Hungary", style={"font-size": "30px", "font-weight": "bold"}),
                html.P("-Population: 9.6 million inhabitants"),
                html.P("-Weather: Cold winters and warm summers"),
                html.P("-Best Year in the olympics: 1952 with 102 medals"),
                html.P("-Worst Year in the olympics: 1904 with 4 medals"),
                html.P("-Inventor of the Rubik's Cube"),
                html.P("-Best water-polo team in history of the sport with 15 olympic medals"),
                html.P("-Did not participate in 1920 and 1984 years Olympic summer games")
            ],
            style={"max-width": "400px", "line-height": "1.5", "font-size": "20px"})
            ]
        ), 
            
} 