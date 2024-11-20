import pandas as pd
import plotly_express as px
import numpy as np

import os
path = os.path.abspath("C:/Code/Project-OS/Data/athlete_events.csv")


df = pd.read_csv(path)

df.sort_values("Year", ascending=False, inplace=True)
#df.dropna(inplace=True)

df_age_by_year = pd.DataFrame()
li = df["Sport"].unique()
for sport in li:
    df_age_by_year[sport] = df[ df["Sport"] == sport ].groupby("Year")["Age"].mean()

df_age_by_year

"""
df.sort_values("Year", ascending=False, inplace=True)
df.dropna(inplace=True)
df_water_craft = df[(df["Sport"]=="Sailing") | (df["Sport"]=="Rowing") | (df["Sport"]=="Canoeing") ] 

df_age_by_year = pd.DataFrame()
li = df["Sport"].unique()
for sport in li:
    df_age_by_year[sport] = df[ df["Sport"] == sport ].groupby("Year")["Age"].mean()
"""
#df_new["Rowing"] = df_water_craft[df.Sport == "Rowing"].groupby("Year")["Age"].mean()
#df_new["Canoeing"] = df_water_craft[df.Sport == "Canoeing"].groupby("Year")["Age"].mean()
#df_new["Sailing"] = df_water_craft[df.Sport == "Sailing"].groupby("Year")["Age"].mean()



#df_new.dropna(inplace=True)

#fig_01 = px.line(df_new, y=["Rowing", "Canoeing", "Sailing"], labels={ "y": "Sport",})
#fig_01 = px.line(df_new, y=["Canoeing", "Rowing", "Sailing"], range_y=[20,40]),
#fig_02 = px.line(df_new, y=["Canoeing", "Rowing"], range_y=[20,40]),
#fig_03 = px.line(df_new, y=["Canoeing"], range_y=[20,40]),



#fig_01.update_layout( yaxis=dict( title=dict( text="Sport")  ) ) 
#fig_01.show()

#----------------------------------------------------------------------

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
"""
hungary_medals["World War I : End"] = 0
hungary_medals.at[1924, "World War I : End",]= 20
hungary_medals["World War II : End"] = np.NaN 
hungary_medals.loc[1948, "World War II : End"] = 18

hungary_medals["Fall of Berlin Wall"] = np.NaN 
hungary_medals.loc[1988, "Fall of Berlin Wall"] = 18
"""
path_adam = os.path.abspath("C:/Code/Project-OS/Adam/")
#hungary_medals = pd.read_csv(r"C:/Code/Project-OS/Adam/hm.csv")
hungary_medals.to_csv(path_adam+'/hm.csv', index=True)

fig = px.line(hungary_medals, y=["Gold", "Silver", "Bronze"], color_discrete_sequence=['Gold', 'Silver', 'Brown'])
