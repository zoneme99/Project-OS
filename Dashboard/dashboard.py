import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


df = pd.read_csv("../Data/athlete_events.csv")
noc_regions = pd.read_csv("../Data/noc_regions.csv")

df = pd.merge(df, noc_regions[['NOC', 'region']], on='NOC', how='left')
df['NOC'] = df['region']
df.drop(columns=['region'], inplace=True)

hungary = df[df["NOC"] == "Hungary"]

medals = df[df["Medal"].notnull()]
medals["Medal"] = medals["Medal"].str.strip()
medals["Unique_Medal_Event"] = medals["Year"].astype(str) + "_" + medals["Event"] + "_" + medals["Medal"]
unique_medals = medals.drop_duplicates(subset=["Unique_Medal_Event"])

medal_distribution = medals.groupby("Medal").size().reset_index(name="Count")
medal_distribution["Medal"] = medal_distribution["Medal"].str.strip()

sports_medals = medals.groupby("Sport").size().reset_index(
    name="Count").sort_values(by="Count", ascending=False).head(10)

age_data = hungary[hungary["Age"].notnull()]


app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'backgroundColor': '#F0FFFF',
        'color': 'black',
        'fontFamily': 'Arial, Helvetica, sans-serif',
        'padding': '20px',
        'height': '100vh',
        'margin': '-0.8vh'
    },
    children=[
        html.H1("Projekt OS", style={'textAlign': 'center', 'color': 'black'}),

        html.Div(
            [
                html.Label("Välj en sport:", style={
                           'textAlign': 'center', 'marginBottom': '1vh'}),
                dcc.Dropdown(
                    id="sport-dropdown",
                    options=[{"label": sport, "value": sport}
                             for sport in df["Sport"].unique()],
                    value="Swimming",
                    style={'textAlign': 'center',
                           'width': '10vw', 'color': 'black'}
                ),
                html.Label("Välj ett land:", style={
                           'textAlign': 'center', 'marginBottom': '1vh', 'marginTop': '1vh'}),
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[
                        {"label": country, "value": country}
                        for country in sorted(df["NOC"].dropna().unique()) if country
                    ],
                    value="Hungary",
                    style={'textAlign': 'center',
                           'width': '10vw', 'color': 'black'}
                ),
            ],
            style={
                'margin': '20px auto',
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
            }
        ),
        dcc.Graph(id="medals-per-os-graph"),
        dcc.Graph(id="sports-medals-graph"),
        dcc.Graph(
            figure=px.histogram(
                age_data,
                x="Age",
                nbins=20,
                title="Åldersfördelning av Ungerns idrottare",
                labels={"Age": "Ålder", "count": "Antal idrottare"}
            ).update_layout(plot_bgcolor="#F0FFFF", paper_bgcolor="#F0FFFF", font=dict(color="black"))
        ),
    ]
)


@app.callback(
    Output("medals-per-os-graph", "figure"),
    [Input("sport-dropdown", "value"), Input("country-dropdown", "value")]
)
def update_medals_per_os(selected_sport, selected_country):
    filtered_data = unique_medals[(unique_medals["Sport"] == selected_sport) & (
        unique_medals["NOC"] == selected_country)]

    if filtered_data.empty:
        fig = px.bar(
            title=f"Inga medaljer för {selected_country} i {selected_sport}"
        )
        fig.update_layout(
            plot_bgcolor="#F0FFFF",
            paper_bgcolor="#F0FFFF",
            font=dict(color="black"),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig

    medals_per_os = filtered_data.groupby(
        ["Year", "Medal"]).size().reset_index(name="Count")

    fig = px.bar(
        medals_per_os,
        x="Year",
        y="Count",
        color="Medal",
        title=f"Medaljer för {selected_country} i {selected_sport} per OS",
        labels={"Year": "År", "Count": "Antal medaljer", "Medal": "Medaljtyp"},
        color_discrete_map={"Gold": "#FFD700",
                            "Silver": "#C0C0C0", "Bronze": "#CD7F32"}
    )

    fig.update_layout(
        plot_bgcolor="#F0FFFF",
        paper_bgcolor="#F0FFFF",
        font=dict(color="black"),
        xaxis=dict(
            tickmode='linear',
            tick0=min(medals_per_os["Year"]),
            dtick=4
        )
    )

    return fig


@app.callback(
    Output("sports-medals-graph", "figure"),
    [Input("country-dropdown", "value")]
)
def update_sports_medals(selected_country):
    filtered_data = unique_medals[unique_medals["NOC"] == selected_country]

    sports_medals = filtered_data.groupby(
        ["Sport", "Medal"]).size().reset_index(name="Count")
    top_sports = sports_medals.groupby(
        "Sport")["Count"].sum().nlargest(10).index
    sports_medals = sports_medals[sports_medals["Sport"].isin(top_sports)]

    fig = px.bar(
        sports_medals,
        x="Sport",
        y="Count",
        color="Medal",
        title=f"Topp 10 sporter där {selected_country} har flest medaljer",
        labels={"Sport": "Sport", "Count": "Antal medaljer",
                "Medal": "Medaljtyp"},
        color_discrete_map={"Gold": "#FFD700",
                            "Silver": "#C0C0C0", "Bronze": "#CD7F32"}
    )

    fig.update_layout(
        plot_bgcolor="#F0FFFF",
        paper_bgcolor="#F0FFFF",
        font=dict(color="black"),
        xaxis=dict(tickangle=-45)
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
