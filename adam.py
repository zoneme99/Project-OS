import pandas as pd
import plotly_express as px
from dash import html, dcc
import dash_bootstrap_components as dbc

# Create your charts here 
df = pd.read_csv("Data/athlete_events.csv") 

def select_sport(selection_of_sport):
    chosen_sport = (df["Sport"] == selection_of_sport) & (df["Medal"].notna())
    medals_by_country = (df[chosen_sport].groupby("NOC")[["Medal"]].count().sort_values(by="Medal",ascending=False).reset_index()) # groups by NOC and counts number of medals, sort values and then resets index.
    return medals_by_country

# ----------------
# Unique_Medals

hungary = df[df["NOC"]=="HUN"]

def  unique_medals( df ):
    set_year_medal_event = set()
    for idx, row in df.dropna( subset=["Medal"] ).iterrows():
        set_year_medal_event.add(f" {row['Year']}|{row['Event']}|{row['Medal']} ")
    len(set_year_medal_event)

    year = [ row.split("|")[0][1:] for row in set_year_medal_event ]
    event = [ row.split("|")[1] for row in set_year_medal_event ]
    medal = [ row.split("|")[2][:-1] for row in set_year_medal_event ]

    df_new = pd.DataFrame(   
        {"Year":year, "Medal":medal, "Event":event}
    ) 

    return df_new

# Hungary Unique Medal Per Event
hungary_ume = unique_medals( hungary )

hungary_ume


# ----------------
# Medals Only
def medals_only( df ):
    df.groupby("Year")["Medal"].count()
    df["Gold"] = df["Medal"] == "Gold" 
    df["Silver"] = df["Medal"] == "Silver" 
    df["Bronze"] = df["Medal"] == "Bronze" 

    return df[["Year","Gold","Silver","Bronze"]].groupby("Year").sum()

hungary_medals = medals_only( hungary_ume  )
hungary_medals


# ----------------

# Example Dataframe
df_info = pd.DataFrame() 
df_info["Hosts"] = "Athens,France,USA,UK,Sweden".split(",")
df_info["Year"] = "1896,1900,1904,1908,1912".split(",")

# I stored the px.line in a variable outside the select dict
# because dash doesn't like that you add .uppdate_layout 
# while you add the graph to the figure element
unique_medals = px.line(
    hungary_medals, y=["Gold", "Silver", "Bronze"], 
    color_discrete_sequence=['Gold', 'Silver', 'Brown']
    ).update_layout(yaxis_title="Number of Medals")


# Add your completed charts to the select dictionary
# select={ 
#   "chart_name_a": dcc.Graph( figure=px.bar(    )), 
#   "chart_name_b": dcc.Graph( figure=px.line(   )),
# }
# the dcc.Graph is the element used by app.layout = [] to display graphs
# the figure= contains the plotly_express chart
# check the tobbe.py file for further references
# NOTE You should be able to add any tipe of object like a string, dash_table or another di

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
         "Unique Medals": dcc.Graph( figure= unique_medals ),
         #Project-OS\olympic_flag_2.png
         #Project-OS\olympic_flag_2.png
         
         "h1_test": html.H1(children="Great Scott"),
         "div_test": html.Div(children=[
             html.Img( style={ "width":"400px", "height":"247px", },  src="https://upload.wikimedia.org/wikipedia/commons/a/a7/Olympic_flag.svg" ),
             dbc.Table.from_dataframe(df_info)
            ]),

}