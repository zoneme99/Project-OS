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


# ----------------
# Medals Only
def medals_only( df ):
    df.groupby("Year")["Medal"].count()
    df["Gold"] = df["Medal"] == "Gold" 
    df["Silver"] = df["Medal"] == "Silver" 
    df["Bronze"] = df["Medal"] == "Bronze" 

    return df[["Year","Gold","Silver","Bronze"]].groupby("Year").sum()


chart_style = {
    'border': '2px solid #444339',
    'border-radius': '6px',
    'margin': '10px'
}

# ----------------

# Example Dataframe
df_info = pd.DataFrame() 
df_info["Hosts"] = "Athens,France,USA,UK,Sweden".split(",")
df_info["Year"] = "1896,1900,1904,1908,1912".split(",")

# I stored the px.line in a variable outside the select dict
# because dash doesn't like that you add .uppdate_layout 
# while you add the graph to the figure element

# Medals Per Year
"""
def medals_per_year( df ):
    return px.line(
    medals_only( unique_medals( df ) ), 
    y=["Gold", "Silver", "Bronze"], 
    color_discrete_map={"Gold": "#FFD700", "Silver": "#C0C0C0", "Bronze": "#CD7F32"}
    ).update_layout(
        yaxis_title="Number of Medals", 
        plot_bgcolor="#EFE1BA", 
        paper_bgcolor="#EFE1BA", 
        font=dict(color="#444339")
    )


medals_per_year_total  = medals_per_year( hungary )
medals_per_year_women  = medals_per_year( hungary[hungary["Sex"]=="F"] )
medals_per_year_men    = medals_per_year( hungary[hungary["Sex"]=="M"] )
medals_per_year_summer = medals_per_year( hungary[hungary["Season"]=="Summer"] )
medals_per_year_winter = medals_per_year( hungary[hungary["Season"]=="Winter"] )

medals_per_year_non  = px.line(
    medals_only( hungary ), 
    y=["Gold", "Silver", "Bronze"], 
    color_discrete_map={"Gold": "#FFD700", "Silver": "#C0C0C0", "Bronze": "#CD7F32"}
    ).update_layout(
        yaxis_title="Number of Medals", 
        plot_bgcolor="#EFE1BA", 
        paper_bgcolor="#EFE1BA", 
        font=dict(color="#444339")
    )

"""
# Mean Age 
"""
df.sort_values("Year", ascending=False, inplace=True)
df_age_by_year = pd.DataFrame()
li = df["Sport"].unique()
for sport in li:
    df_age_by_year[sport] = df[ df["Sport"] == sport ].groupby("Year")["Age"].mean()

df_age_by_year["Water Polo"]  = (df_age_by_year["Water Polo"].bfill()+df_age_by_year["Water Polo"].ffill())/2 

mean_age = px.line( 
    df_age_by_year[["Fencing","Gymnastics","Water Polo"]],  
    color_discrete_map={"Fencing": "#32cd6d", "Gymnastics": "#cd3292", "Water Polo": "#3294cd"}
    ).update_layout( 
        yaxis_title="Maen Age",
        plot_bgcolor="#EFE1BA",
        paper_bgcolor="#EFE1BA", 
        font=dict(color="#444339")
    )

mean_age
"""
# Medals Ratio
"""
def medals_ratio( df:"DataFrame", noc:str  )->"DataFrame":
    df_noc = medals_only( unique_medals( df[df["NOC"]==noc]) )
    df_all = medals_only( unique_medals( df ) )
    df_noc["Gold (%)"] = df_noc.apply(lambda x: round(x["Gold"]/df_all.loc[x.name]["Gold"]*100, 1), axis=1) 
    df_noc["Silver (%)"] = df_noc.apply(lambda x: round(x["Silver"]/df_all.loc[x.name]["Silver"]*100, 1), axis=1) 
    df_noc["Bronze (%)"] = df_noc.apply(lambda x: round(x["Bronze"]/df_all.loc[x.name]["Bronze"]*100, 1), axis=1) 
    df_noc["Medals (%)"] = df_noc.apply(lambda x: round((x["Gold"]+x["Silver"]+x["Bronze"])/(df_all.loc[x.name]["Gold"]+df_all.loc[x.name]["Silver"]+df_all.loc[x.name]["Bronze"])*100, 1), axis=1)
    df_noc["World (%)"] = 100-df_noc["Medals (%)"]
    return df_noc

hungary_medals = medals_ratio( df, "HUN")
sweden_medals = medals_ratio( df, "SWE")

hungary_medals
sweden_medals

medals_per_year_ratio = px.bar( 
        hungary_medals, y=["Medals (%)","World (%)"],  
        color_discrete_map={"Medals (%)": "#5f5c4d", "World (%)": "#bcb092"}
    ).update_layout( 
        yaxis_title="Maen Age",
        plot_bgcolor="#EFE1BA",
        paper_bgcolor="#EFE1BA", 
        font=dict(color="#444339")
    )
"""
# Test 
sailing = px.bar(
    select_sport("Sailing"),
    x="NOC",
    y="Medal",
    color="NOC",
    title= f"Medal overview in Sailing"
    ).update_layout( 
        plot_bgcolor="#EFE1BA", 
        paper_bgcolor="#EFE1BA",
        font=dict(color="#444339")
    )

canoeing = px.bar(
    select_sport("Canoeing"),
    x="NOC",
    y="Medal",
    color="NOC",
    title= f"Medal overview in Canoeing"
    ).update_layout( 
        plot_bgcolor="#EFE1BA",
        paper_bgcolor="#EFE1BA", 
        font=dict(color="#444339")
    )





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
        "Sailing": dcc.Graph( figure=sailing,style=chart_style ),
        "Canoeing": dcc.Graph( figure=canoeing, style=chart_style ),
        #"Mean Age": dcc.Graph( figure=mean_age, style=chart_style ),

       # "Medals Per Year : Ratio" : dcc.Graph( figure=medals_per_year_ratio, style=chart_style ),

      #  "Medals Per Year : Total": dcc.Graph( figure=medals_per_year_total, style=chart_style ),
      #  "Medals Per Year : Non-Unique": dcc.Graph( figure=medals_per_year_non, style=chart_style ),
      #  "Medals Per Year : Women": dcc.Graph( figure=medals_per_year_women, style=chart_style ),
      #  "Medals Per Year : Men": dcc.Graph( figure=medals_per_year_men, style=chart_style ),
      #  "Medals Per Year : Summer": dcc.Graph( figure=medals_per_year_summer, style=chart_style ),
      #  "Medals Per Year : Winter": dcc.Graph( figure=medals_per_year_winter, style=chart_style ),
    
        "h1_test": html.H1(children="Great Scott"),
        "div_test": html.Div(children=[
             html.Img( style={ "width":"400px", "height":"247px", },  src="https://upload.wikimedia.org/wikipedia/commons/a/a7/Olympic_flag.svg" ),
             dbc.Table.from_dataframe(df_info)
            ]),

}