import pandas as pd
import plotly_express as px

import os
path = os.path.abspath("C:/Code/Project-OS/Data/athlete_events.csv")
df = pd.read_csv(path)

hungary = df[df["NOC"]=="HUN"]


def  unique_medals( df ):
    set_year_medal_event = set()
    for idx, row in df.dropna( subset=["Medal"] ).iterrows():
        set_year_medal_event.add(f" {row['Year']}|{row['Event']}|{row['Medal']} ")
    len(set_year_medal_event)

    year = [ row.split("|")[0][1:] for row in set_year_medal_event ]
    event = [ row.split("|")[1] for row in set_year_medal_event ]
    medal = [ row.split("|")[2][:-1] for row in set_year_medal_event ]

    df_um = pd.DataFrame(   
        {"Year":year, "Medal":medal, "Event":event}
    ) 

    return df_um
hungary_medals_per_event = unique_medals( hungary )



def medals_only( df ):
    df.groupby("Year")["Medal"].count()
    df["Gold"] = df["Medal"] == "Gold" 
    df["Silver"] = df["Medal"] == "Silver" 
    df["Bronze"] = df["Medal"] == "Bronze" 

    return df[["Year","Gold","Silver","Bronze"]].groupby("Year").sum()

hungary_medals = medals_only( hungary_medals_per_event  )

fig = px.line(hungary_medals, y=["Gold", "Silver", "Bronze"], color_discrete_sequence=['Gold', 'Silver', 'Brown'])
