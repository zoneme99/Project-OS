import pandas as pd
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc
import hashlib as hl


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

# This retruns None incase there is a missing name ???
def hash_name(name):
    if (name == None):
        return None
    return hl.sha256(name.encode()).hexdigest()

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


# There are two of these 
# I believe neither of them is in use 
# [
def select_sport(sport):
    filtered = (df["Sport"] == sport) & (df["Medal"].notna())
    return df[filtered].groupby("NOC")[["Medal"]].count().sort_values(by="Medal", ascending=False).reset_index()
# ]

# Not in use?
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

# Does this part do anything ?
# connected to Top 10 Sports Where Hungary Won Medals
# [
hungary = df[df["NOC"] == "Hungary"]
medals = hungary[hungary["Medal"].notnull()]

total_medals_by_sport = medals.groupby(
    "Sport").size().reset_index(name="Count")

top_sports = total_medals_by_sport.sort_values(
    by="Count", ascending=False).head(10)
# ] 

hungary_medals_per_year = medals_per_year(unique_medals, "Hungary")
hungary_medal_distribution = medal_distribution(unique_medals)

# Maybe Already Exits
# Connected to 'Top 10 Sports Where Hungary Won Medals'
# [
df_sorted = df.sort_values("Year", ascending=False)
df_age_by_year = pd.DataFrame()
li = df["Sport"].unique()
for sport in li:
    df_age_by_year[sport] = df_sorted[df_sorted["Sport"] == sport].groupby("Year")[
        "Age"].mean()

df_age_by_year["Water Polo"] = (
    df_age_by_year["Water Polo"].bfill()+df_age_by_year["Water Polo"].ffill())/2
# ]

# Not in Use ?
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
    # Works
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
    # Works
    "Medal Distribution For Hungary": dcc.Graph(
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
    # Works but the interface is a little buggy
    "Average Age : Fencing / Gymnastics / Water Polo": dcc.Graph(
        figure=px.line(
            df_age_by_year[["Fencing", "Gymnastics", "Water Polo"]],
            color_discrete_map={"Fencing": "#32cd6d",
                                "Gymnastics": "#cd3292", "Water Polo": "#3294cd"}
        ).update_layout(plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339")),
        style=chart_style
    ),
    # Works
    "Medals Won by Hungary by Year": dcc.Graph(
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
    # Works but the interface is a little buggy
    "Top 10 Sports Where Hungary Won Medals": dcc.Graph(
        figure=px.bar(
            top_sports,
            x="Sport",
            y="Count",
            color="Sport",
            title="Top 10 Sports Where Hungary Won Medals",
        ).update_layout(plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339")),
        style=chart_style
    ),
    # Works but the interface is a little buggy
    "Gold Fencing Men": dcc.Graph(
        figure=px.pie(
            values=[len(df[(df["Sex"] == "M") & (df["Sport"] == "Fencing") & (df["Medal"] == "Gold")]),
                    len(df[(df["Sex"] == "M") & (df["Sport"] == "Fencing") & (df["Medal"] == "Gold") & (df["NOC"] == "Hungary")])],
            names=["Other Men", "Hungarian Men"],
            title="Gold Medals in Fencing"
        ).update_layout(plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339")),
        style=chart_style
    ),
    # Works
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
                                "-Best Year in the olympics: 1952 with 102 medals"),
                            html.P(
                                "-Worst Year in the olympics: 1904 with 4 medals"),
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
