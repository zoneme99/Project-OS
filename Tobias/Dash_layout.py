import pandas as pd
import plotly_express as px
from dash import Dash,html, dcc, dash_table
from dash.dependencies import Input, Output



df = pd.read_csv("../Tobias/athlete_events.csv")            # Reading in the csv-file(dataset)

# hungary = df[df["Team"] == "Hungary"]


app = Dash(__name__)                                        # Initialize app


app.layout = [                                              # layout-design
    html.Div(children = "Project OS", style={"text-align": "center"}),
    dash_table.DataTable(data=df.to_dict("records"), page_size=10
    ),

    html.Hr(),
    
    dcc.Dropdown(                                                                       # Dropdown on dash, with labels and values.
    id="Sport dropdown",
    options= [
            {"label": "Weightlifting", "value": "Weightlifting"},
            {"label": "Archery", "value": "Archery"},
            {"label": "Gymnastics", "value": "Gymnastics"},
            {"label": "Age distribution with medals", "value": "Age distribution"}
            ],
    placeholder="Select a sport",                                                       # Gives dropdown a "default text"
    
    ),
    dcc.Graph(
        id="Medal chart",
        
    )    
]

@app.callback(                                                                  # Gives the dashapp input and output, user input linked with app output.
    Output("Medal chart", "figure"),
    Input("Sport dropdown", "value")
)

def medal_chart(selection_of_sport):

    if not selection_of_sport:                                                  # if no choice - show empty graph.
        return {}
    
    if selection_of_sport == "Age distribution":                                # if age distribution is chosen, generates boxplot.
        chosen_sports = ["Weightlifting", "Archery", "Gymnastics"]
        return age_distribution(chosen_sports)
    
    chosen_sport = (df["Sport"] == selection_of_sport) & (df["Medal"].notna())
    medals_by_country = (df[chosen_sport].groupby("NOC")[["Medal"]].count().sort_values(by="Medal",ascending=False).reset_index() # groups by NOC and counts number of medals, sort values and then resets index.
    )

    fig= px.bar(
        medals_by_country,
        x="NOC",
        y="Medal",
        color="NOC",
        title= f"Medal overview in {selection_of_sport}"
    )
    return fig

def age_distribution(chosen_sports):                                                        # Function for boxplot, age-distribution and filtering data with groupby.
    filt_df = df[df["Sport"].isin(chosen_sports)]
    age_distribution = filt_df.groupby("Sport")[["Age", "Medal"]].describe()
    age_distribution

    fig = px.box(filt_df, 
                x="Sport", 
                y="Age",
                color="Medal", 
                title="Age distribution in Weightlifting, Archery and Gymnastics")
    
    
    return fig



if __name__ == "__main__":                                  # Runs the app
    app.run(debug=True)