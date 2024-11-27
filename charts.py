import pandas as pd
import plotly.express as px
from dash import html, dcc
import hashlib as hl
import numpy as np


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

# Medaljfärger
medal_colors = {
    "Gold": "#FFD700",
    "Silver": "#C0C0C0",
    "Bronze": "#CD7F32"
}


olympic_years = df["Year"].unique()
olympic_years = sorted(olympic_years)


def hash_name(name):
    if (name == None):
        return None
    return hl.sha256(name.encode()).hexdigest()


df.loc[df.index, "Name"] = df["Name"].apply(hash_name)
hungary = df[df["NOC"] == "Hungary"].copy()

# Removes all athletes that didn't win a medal
# Combines the Year Medal and Event in to a new column named Unique_Medal_Event
# Removes all rows with the same Unique_Medal_Event value, except one
# this way you're left with only one medal of each value per event.


def medals_only(df):
    medals = df[df["Medal"].notnull()].copy()
    medals["Unique_Medal_Event"] = medals["Year"].astype(
        str) + "_" + medals["Event"] + "_" + medals["Medal"]
    medals.drop_duplicates(subset=["Unique_Medal_Event"], inplace=True)
    medals.drop(columns=["Unique_Medal_Event"], inplace=True)
    return medals


unique_medals = medals_only(df)


def medal_distribution(unique_medals):
    return unique_medals.groupby("Medal").size().reset_index(name="Count")


def medals_per_year(unique_medals, country):
    filtered_data = unique_medals[unique_medals["NOC"] == country]
    return filtered_data.groupby(["Year", "Medal"]).size().reset_index(name="Count")


# Returns a DataFrame summing up all the medals the
# countires have take year by year.
# Argument noc : The countires you want be returned
# Argument ratio : Set to true to conver the number of medals in to percentage.


def get_medals_only(noc: list, ratio: bool = False):
    unique_medals = medals_only(df[df["Season"] == "Summer"])
    medals = pd.DataFrame(index=unique_medals["Year"])
    medals = unique_medals[unique_medals["NOC"].isin(noc)].groupby(
        ["Year", "NOC"]).size().unstack().copy()

    # This line gives us the medals won by the entire world except for the chosen countries
    medals["World"] = unique_medals.groupby(
        "Year")["Medal"].size()-medals.apply(np.sum, axis=1)
    if ratio:
        medals["Total"] = medals.apply(np.sum, axis=1)
        for _ in noc+["World"]:
            medals[_] = (medals[_]*100)/medals["Total"]
        medals.drop(columns=["Total"], inplace=True)
    return medals


medals_ratio = get_medals_only(["Hungary", "Sweden", "USA"], True)

medals = hungary[hungary["Medal"].notnull()]

total_medals_by_sport = medals.groupby(
    "Sport").size().reset_index(name="Count")

top_sports = total_medals_by_sport.sort_values(
    by="Count", ascending=False).head(10)

df_top_unique = unique_medals[unique_medals["NOC"] == "Hungary"].groupby(
    "Sport", as_index=False)["Medal"].count()
df_top_unique.sort_values("Medal", ascending=False, inplace=True)


hungary_medals_per_year = medals_per_year(unique_medals, "Hungary")
hungary_medal_distribution = medal_distribution(
    unique_medals[unique_medals["NOC"] == "Hungary"])
hungary_medal_distribution["Medal"] = hungary_medal_distribution["Medal"].str.strip(
)


df_mean_age = df[(df["Sport"] == "Water Polo") | (df["Sport"] == "Gymnastics") | (
    df["Sport"] == "Fencing")].groupby(["Year", "Sport"])["Age"].mean()
df_mean_age = df_mean_age.unstack()
df_mean_age["Water Polo"] = (
    df_mean_age["Water Polo"].bfill()+df_mean_age["Water Polo"].ffill())/2


def age_distribution(chosen_sports):
    filt_df = df[df["Sport"].isin(chosen_sports)]

    return filt_df


def fencing_gold_by_noc():
    gold = df[(df['Medal'] == 'Gold') & (df['Sport'] == 'Fencing')
              ].groupby('NOC')['Medal'].count()
    gold = gold.sort_values(ascending=False)
    return [*gold.iloc[0:3], gold.iloc[3:].sum()], ['Italy', 'France', 'Hungary', 'Other']


select = {
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
                                "-Worst Year in the olympics: 1896 and 1904 with 4 medals"),
                            html.P("-Inventor of the Rubik's Cube"),
                            html.P(
                                "-Did not participate in 1920 and 1984 years Olympic summer games"),
                            html.P(
                                "-Best water-polo team in history of the sport with 15 olympic medals"),
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
    "Gold Fencing Men": dcc.Graph(
        figure=px.pie(
            values=fencing_gold_by_noc()[0],
            names=fencing_gold_by_noc()[1],
            title="Gold Medals in Fencing"
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
    "Medals Won by Year": dcc.Graph(
        figure=px.bar(
            hungary_medals_per_year,
            x="Year",
            y="Count",
            color="Medal",
            title="Medals for Hungary by Type per Year",
            color_discrete_map=medal_colors
        ).update_layout(
            plot_bgcolor="#EFE1BA",
            paper_bgcolor="#EFE1BA",
            font=dict(color="#444339"),
            xaxis=dict(
                tickvals=olympic_years,
                title="Year"
            )
        ),
        style=chart_style
    ),
    "Medal Distribution": dcc.Graph(
        figure=px.pie(
            hungary_medal_distribution,
            names="Medal",
            values="Count",
            title="Medal Distribution for Hungary",
            color="Medal",
            color_discrete_map=medal_colors
        ).update_layout(plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339")),
        style=chart_style
    ),
    "Percentage of Medals": dcc.Graph(
        figure=px.bar(
            medals_ratio,
            color_discrete_map={
                "Hungary": "#3f8c37", "World": "#bcb092", "USA": "#c73434", "Sweden": "#37518c"},
            title="Percentage of Medals Won During Summer Games             Pop 2016 : USA 323m | Sweden 10m |  Hungary 10m ",
        ).update_layout(yaxis_title="Medals (%)", plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339"), xaxis=dict(
            tickvals=olympic_years,
            title="Year"
        )),
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
    "Age Distribution": dcc.Graph(
        figure=px.box(
            age_distribution(["Fencing", "Water Polo", "Gymnastics"]),
            x="Sport",
            y="Age",
            color="Medal",
            title="Age distribution in Fencing, Water Polo, and Gymnastics",
            color_discrete_map=medal_colors
        ).update_layout(plot_bgcolor="#EFE1BA", paper_bgcolor="#EFE1BA", font=dict(color="#444339")),
        style=chart_style
    ),
}
