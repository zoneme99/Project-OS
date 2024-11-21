import pandas as pd
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc


df = pd.read_csv("Data/athlete_events.csv")
noc_regions = pd.read_csv("Data/noc_regions.csv")


df = pd.merge(df, noc_regions[['NOC', 'region']], on='NOC', how='left')
df['NOC'] = df['region']
df.drop(columns=['region'], inplace=True)


hungary = df[df["NOC"] == "Hungary"]

chart_style = {
    'border': '2px solid #444339',
    'border-radius': '6px',
    'margin': '10px'
}


def medals_only(df):
    medals = df[df["Medal"].notnull()].copy()
    medals["Medal"] = medals["Medal"].str.strip()
    medals["Unique_Medal_Event"] = medals["Year"].astype(
        str) + "_" + medals["Event"] + "_" + medals["Medal"]
    unique_medals = medals.drop_duplicates(subset=["Unique_Medal_Event"])
    return unique_medals


unique_medals = medals_only(df)


def medal_distribution(unique_medals):
    return unique_medals.groupby("Medal").size().reset_index(name="Count")


hungary_medal_distribution = medal_distribution(unique_medals)


def top_sports_medals(unique_medals):
    sports_medals = unique_medals.groupby(
        "Sport").size().reset_index(name="Count")
    return sports_medals.sort_values(by="Count", ascending=False).head(10)


hungary_top_sports = top_sports_medals(unique_medals)


def medals_per_year(unique_medals, country):
    filtered_data = unique_medals[unique_medals["NOC"] == country]
    grouped = filtered_data.groupby(
        ["Year", "Medal"]).size().reset_index(name="Count")
    return grouped


hungary_medals_per_year = medals_per_year(unique_medals, "Hungary")


hungary_line_graph = px.bar(
    hungary_medals_per_year,
    x="Year",
    y="Count",
    color="Medal",
    title="Medals for Hungary by Type per Year",
    color_discrete_map={"Gold": "#FFD700",
                        "Silver": "#C0C0C0", "Bronze": "#CD7F32"}
).update_layout(plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339"))

hungary_medal_distribution = px.pie(
    hungary_medal_distribution,
    names="Medal",
    values="Count",
    title="Medal Distribution for Hungary",
    color="Medal",
    color_discrete_map={
        "Gold": "#FFD700",
        "Silver": "#C0C0C0",
        "Bronze": "#CD7F32"
    }
).update_layout(
    plot_bgcolor="#EFE1BA",
    paper_bgcolor="#EFE1BA",
    font=dict(color="#444339")
)


def sports_medals_overview(unique_medals, country):
    filtered_data = unique_medals[unique_medals["NOC"] == country]
    sports_medals = filtered_data.groupby(
        ["Sport", "Medal"]).size().reset_index(name="Count")
    top_sports = sports_medals.groupby(
        "Sport")["Count"].sum().nlargest(10).index
    return sports_medals[sports_medals["Sport"].isin(top_sports)]


hungary_sports_overview = sports_medals_overview(unique_medals, "Hungary")

hungary_sports_graph = px.bar(
    hungary_sports_overview,
    x="Sport",
    y="Count",
    color="Medal",
    title="Top 10 Sports Where Hungary Won Medals",
    color_discrete_map={"Gold": "#FFD700",
                        "Silver": "#C0C0C0", "Bronze": "#CD7F32"}
).update_layout(plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339"))

df_info = pd.DataFrame()
df_info["Hosts"] = "Athens,France,USA,UK,Sweden".split(",")
df_info["Year"] = "1896,1900,1904,1908,1912".split(",")


select = {
    "Medal Distribution For Hungary": dcc.Graph(
        figure=hungary_medal_distribution,
        style=chart_style
    ),
    "Hungary's Top Sports": dcc.Graph(
        figure=hungary_sports_graph,
        style=chart_style
    ),
    "Medals Won by Hungary by Year": dcc.Graph(
        figure=hungary_line_graph,
        style=chart_style
    ),
}
