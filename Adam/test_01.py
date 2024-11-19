import pandas as pd
import plotly_express as px

import os
path = os.path.abspath("C:/Code/Project-OS/Data/athlete_events.csv")


df = pd.read_csv(path)

df.sort_values("Year", ascending=False, inplace=True)
df.dropna(inplace=True)
df_water_craft = df[(df["Sport"]=="Sailing") | (df["Sport"]=="Rowing") | (df["Sport"]=="Canoeing") ] 

df_new = pd.DataFrame()
df_new["Rowing"] = df_water_craft[df.Sport == "Rowing"].groupby("Year")["Age"].mean()
df_new["Canoeing"] = df_water_craft[df.Sport == "Canoeing"].groupby("Year")["Age"].mean()
df_new["Sailing"] = df_water_craft[df.Sport == "Sailing"].groupby("Year")["Age"].mean()
df_new.dropna(inplace=True)
#fig_01 = px.line(df_new, y=["Rowing", "Canoeing", "Sailing"], labels={ "y": "Sport",})
fig_01 = px.line(df_new, y=["Rowing", "Canoeing", "Sailing"], range_y=(20,40))
#fig_01.update_layout( yaxis=dict( title=dict( text="Sport")  ) ) 
#fig_01.show()

