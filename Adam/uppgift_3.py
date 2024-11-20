from dash import Dash, html, dash_table, dcc, Input, Output,callback
import plotly.express as px
import pandas as pd 
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import test_01
import test_02

df = pd.read_csv("C:/Code/Project-OS/Data/athlete_events.csv")
hungary = df[ df["NOC"] == "HUN" ]

templates=[
    "cyborg"
]

load_figure_template(templates)

#fig = px.bar(hungary, x="Year", y="Medal", color="City", barmode="group", template="CYBORG")
fig = px.bar(hungary, x="Year", y="Medal", color="City", barmode="group", template="cyborg")

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG] ) 

alert = dbc.Alert( "Hello, Bootstrap!", className="m-5" ) 

table = dbc.Table.from_dataframe(
    hungary.head(),
    # using the same table as in the above example
    bordered=True,
    dark=True,
    hover=True,
    responsive=True,
    striped=True,

)
header = html.H4(

    "Project OS", title="Red", id="title", className="bg-primary text-white p-2 mb-2 text-center" 
)
header_2 = html.H5(
    "Hungary",
    className="bg-secondary text-white p-2 mb-2 text-center"
)

dropdown = html.Div(
    [
    #    dbc.Label("Select"),
        dcc.Dropdown(
            #options = ["Canoeing-Rowin-Sailing", "Canoeing-Rowing", "Canoeing"],
            id="indicator",
            options = [
                {"label":"Medals","value":"Medals"}, 
                {"label":"Canoeing-Rowin-Sailing","value":"Canoeing-Rowin-Sailing"}, 
            ],
            placeholder = "Select Graph",
            clearable=False
        ),
    ],
    className="mb-4"
)

radio = dcc.Checklist(
        id="checklist",
        options=["Rowing","Canoeing","Sailing"],
        value=["Rowing","Canoeing","Sailing"],
        inline=True )

#['Rowing', 'Sailing','Canoeing'], 'Rowning')

app.layout = [ 
    #alert,
    header,
    header_2,

    dropdown,
    radio,
    #table,
    dcc.Graph(
        id='example-graph',
        #figure=test_01.fig_01,
        figure = px.line()
       
        #label="Bar Chart"
    ),


    ]

dff = pd.read_csv("C:/Code/Project-OS/Adam/hm.csv")
@callback(
    Output('example-graph', 'figure'),
    Output('title', 'title'),
    Input('indicator', 'value'),
    Input('checklist', 'value'),
    
)
def update_output(indicator, checklist):
    #fig_01 = px.line(test_01.df_new, y=["Rowing", "Canoeing", "Sailing"])
    item={
        "Medals":px.line(dff, y=["Gold", "Silver", "Bronze"], x="Year", color_discrete_sequence=['Gold', 'Silver', 'rgb(217,95,2)']).update_layout(yaxis_title="Number of Medals"),
        "Canoeing-Rowin-Sailing":px.line(test_02.df_new, y=checklist, range_y=[20,40], range_x=[1948,2016]).update_layout(
        yaxis_title="Age"),}

    
    #return px.line(test_01.df_new, y=["Rowing", "Canoeing"])
    
    return item.get(indicator, px.line()), "".join(checklist )


app.run(debug=True)

if __name__ == "maine":
    app.run(debug=True)
