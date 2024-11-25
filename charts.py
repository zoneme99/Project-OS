import pandas as pd
import plotly.express as px
from dash import html, dcc
import hashlib as hl
import numpy as np
# !!! Remove Comment before Render
# Används inte, ta bort?
# [
import dash_bootstrap_components as dbc
# ]



df = pd.read_csv("Data/athlete_events.csv")
noc_regions = pd.read_csv("Data/noc_regions.csv")

# Replaces the NOC style region names with propper names 
# aka SWE becomes Sweden, HUN becomes Hungary.
df = pd.merge(df, noc_regions[['NOC', 'region']], on='NOC', how='left')
df['NOC'] = df['region']
df.drop(columns=['region'], inplace=True)

# We set the style elment in the dcc.Graph objects to 
# this to create a border around the charts.
chart_style = {
    'border': '2px solid #444339',
    'border-radius': '6px',
    'margin': '10px'
}

hungary = df[df["NOC"] == "Hungary"].copy()

# !!! Remove Comment before Render
# This retruns None incase there is a missing name ???
def hash_name(name):
    if (name == None):
        return None
    return hl.sha256(name.encode()).hexdigest()

# !!! Remove Comment before Render
# Got rid of the error message:
# 'A value is trying to be set on a copy of a slice from a DataFrame.'
# by adding .loc
# I think Tobbe fixed this with .copy, but maybe he didn't push it?
df.loc[df.index, "Name"] = df["Name"].apply(hash_name)

# Removes all athletes that didn't win a medal
# Combines the Year Medal and Event in to a new column named Unique_Medal_Event
# Removes all rows with the same Unique_Medal_Event value, except one 
# this way you're left with only one medal of each value per event.
def medals_only(df):
    medals = df[df["Medal"].notnull()].copy()
    medals["Unique_Medal_Event"] = medals["Year"].astype(str) + "_" + medals["Event"] + "_" + medals["Medal"]
    medals.drop_duplicates(subset=["Unique_Medal_Event"], inplace=True)
    medals.drop(columns=["Unique_Medal_Event"], inplace=True)
    return medals

unique_medals = medals_only(df)

# !!! Remove Comment before Render
# The Variable that accesses these function
# are placed at row 92 and 93 
# It might be more clear if we put the variables next to 
# the functions
# [
def medal_distribution(unique_medals):
    return unique_medals.groupby("Medal").size().reset_index(name="Count")


def medals_per_year(unique_medals, country):
    filtered_data = unique_medals[unique_medals["NOC"] == country]
    return filtered_data.groupby(["Year", "Medal"]).size().reset_index(name="Count")
# ]


# !!! Remove Comment before Render
# There are two of these and I believe neither of them is in use 
# [
def select_sport(sport):
    filtered = (df["Sport"] == sport) & (df["Medal"].notna())
    return df[filtered].groupby("NOC")[["Medal"]].count().sort_values(by="Medal", ascending=False).reset_index()
# ]

# !!! Remove Comment before Render
# Not in use, remove?
# Could be usefull if one wants to make a line chart 
# This function gets over written att line 111
# [
def medals_ratio(df, noc):
    df_noc = medals_only(df[df["NOC"] == noc])
    df_all = medals_only(df)
    ratio = pd.DataFrame()
    ratio["Gold (%)"] = df_noc["Gold"] / df_all["Gold"] * 100
    ratio["Silver (%)"] = df_noc["Silver"] / df_all["Silver"] * 100
    ratio["Bronze (%)"] = df_noc["Bronze"] / df_all["Bronze"] * 100
    return ratio
# ] 

# Returns a DataFrame summing up all the medals the 
# countires have take year by year.
# Argument noc : The countires you want be returned
# Argument ratio : Set to true to conver the number of medals in to percentage.
def get_medals_only(noc:list, ratio:bool=False):
    unique_medals = medals_only(df[ df["Season"]=="Summer" ])
    medals = pd.DataFrame( index=unique_medals["Year"] )
    medals = unique_medals[ unique_medals["NOC"].isin(noc) ].groupby(["Year","NOC"]).size().unstack().copy()
    medals["World"] = unique_medals.groupby("Year")["Medal"].size()-medals.apply(np.sum, axis=1)
    if ratio: 
        medals["Total"] = medals.apply(np.sum, axis=1)
        for _ in noc+["World"]:
            medals[_] =  (medals[_]*100)/medals["Total"]
        medals.drop( columns=["Total"], inplace=True)
    return medals

medals_ratio = get_medals_only(["Hungary","Sweden","USA"], True)


hungary = df[df["NOC"] == "Hungary"]
medals = hungary[hungary["Medal"].notnull()]

total_medals_by_sport = medals.groupby(
    "Sport").size().reset_index(name="Count")

top_sports = total_medals_by_sport.sort_values(
    by="Count", ascending=False).head(10)

df_top_unique = unique_medals[ unique_medals["NOC"]=="Hungary" ].groupby("Sport", as_index=False)["Medal"].count()
df_top_unique.sort_values("Medal", ascending=False, inplace=True)


hungary_medals_per_year = medals_per_year(unique_medals, "Hungary")
hungary_medal_distribution = medal_distribution(unique_medals)


df_mean_age = df[ (df["Sport"] == "Water Polo") |  (df["Sport"] == "Gymnastics") | (df["Sport"] == "Fencing")].groupby(["Year","Sport"])["Age"].mean()
df_mean_age = df_mean_age.unstack()
df_mean_age["Water Polo"] = (df_mean_age["Water Polo"].bfill()+df_mean_age["Water Polo"].ffill())/2


# !!! Remove Comment before Render
# Not in Use? Remvoe
# [ 
def select_sport(selection_of_sport):
    chosen_sport = (df["Sport"] == selection_of_sport) & (df["Medal"].notna())
    # groups by NOC and counts number of medals, sort values and then resets index.
    medals_by_country = (df[chosen_sport].groupby("NOC")[["Medal"]].count(
    ).sort_values(by="Medal", ascending=False).reset_index())
    return medals_by_country
# ]

def age_distribution(chosen_sports):
    filt_df = df[df["Sport"].isin(chosen_sports)]

    return filt_df


select = {
    "Age distribution": dcc.Graph(
        figure=px.box(age_distribution(["Fencing", "Water Polo", "Gymnastics"]),
                      x="Sport",
                      y="Age",
                      color="Medal",
                      title="Age distribution in Fencing, Water Polo, and Gymnastics",
                      color_discrete_map={"Gold": "#FFD700",
                                          "Silver": "#C0C0C0", "Bronze": "#CD7F32"}
                      ).update_layout(plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339")),
        style=chart_style

    ),
    "Medal Distribution": dcc.Graph(
        figure=px.pie(
            hungary_medal_distribution,
            names="Medal",
            values="Count",
            title="Medal Distribution for Hungary",
            color_discrete_map={"Gold": "#FFD700",
                                "Silver": "#C0C0C0", "Bronze": "#CD7F32"}
        ).update_layout(plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339")),
        style=chart_style
    ),
    "Average Age": dcc.Graph(
        figure=px.line(
            df_mean_age,
            title="Average Age",
            color_discrete_map={"Fencing": "#32cd6d",
                                "Gymnastics": "#cd3292", "Water Polo": "#3294cd"}
        ).update_layout(yaxis_title="Age", plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339")),
        style=chart_style
    ),
    "Medals Won by Year": dcc.Graph(
        figure=px.bar(
            hungary_medals_per_year,
            x="Year",
            y="Count",
            color="Medal",
            title="Medals for Hungary by Type per Year",
            color_discrete_map={"Gold": "#FFD700",
                                "Silver": "#C0C0C0", "Bronze": "#CD7F32"}
        ).update_layout(plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339")),
        style=chart_style
    ),
    "Percentage of Medals": dcc.Graph(
        figure = px.bar(
            medals_ratio, 
            color_discrete_map={"Hungary": "#3f8c37", "World": "#bcb092","USA":"#c73434", "Sweden":"#37518c" },
            title="Percentage of Medals Won During Summer Games             Pop 2016 : USA 323m | Sweden 10m |  Hungary 10m ",
        ).update_layout( yaxis_title="Medals (%)", plot_bgcolor="#EFE1BA",paper_bgcolor="#EFE1BA", font=dict(color="#444339")),
        style=chart_style
    ),
    "Top 10 Sports": dcc.Graph(
        figure=px.bar(
            top_sports,
            x="Sport",
            y="Count",
            color="Sport",
            title="Top 10 Sports Where Hungary Won Medals",
        ).update_layout(plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339")),
        style=chart_style
    ),
    "Top 10 Sports Unique": dcc.Graph(
        figure=px.bar(
            df_top_unique.head(10),
            x="Sport",
            y="Medal",
            color="Sport",
            title="Top 10 Sports Where Hungary Won Medals (Counting only one medal per Team) ",
        ).update_layout(plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339")),
        style=chart_style
    ),
    "Gold Fencing Men": dcc.Graph(
        figure=px.pie(
            values=[len(df[(df["Sex"] == "M") & (df["Sport"] == "Fencing") & (df["Medal"] == "Gold")]),
                    len(df[(df["Sex"] == "M") & (df["Sport"] == "Fencing") & (df["Medal"] == "Gold") & (df["NOC"] == "Hungary")])],
            names=["Other Men", "Hungarian Men"],
            title="Gold Medals in Fencing"
        ).update_layout(plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339")),
        style=chart_style
    ),
    "Hungary Overview": html.Div(
        style={
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
            "height": "100%",
        },
        children=[
            html.Div(
                style={"display": "flex",
                       "align-items": "center", "gap": "20px"},
                children=[
                    html.Img(
                        style={"width": "400px", "height": "247px",
                               "border": "3px solid black", "display": "block"},
                        src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Flag_of_Hungary.svg"
                    ),
                    html.Img(
                        style={"width": "400px", "height": "247px",
                               "border": "3px solid black", "display": "block"},
                        src="https://upload.wikimedia.org/wikipedia/commons/a/a7/Olympic_flag.svg"
                    ),
                    html.Div(
                        children=[
                            html.H3(
                                "Hungary",
                                style={"font-size": "30px",
                                       "font-weight": "bold"}
                            ),
                            html.P("-Population: 9.6 million inhabitants"),
                            html.P("-Weather: Cold winters and warm summers"),
                            html.P(
                                "-Best Year in the olympics: 1952 with 43 medals"),
                            html.P(
                                "-Worst Year in the olympics: 1896 with 4 medals"),
                            html.P("-Inventor of the Rubik's Cube"),
                            html.P(
                                "-Best water-polo team in history of the sport with 15 olympic medals"),
                            html.P(
                                "-Did not participate in 1920 and 1984 years Olympic summer games"),
                        ],
                        style={
                            "max-width": "400px",
                            "line-height": "1.5",
                            "font-size": "20px",
                            'backgroundColor': "#EFE1BA",
                            'border': '2px solid #444339',
                            'border-radius': '6px',
                            'padding': '10px',
                        }
                    )
                ]
            )
        ]
    )

}
