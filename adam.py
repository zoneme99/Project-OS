import pandas as pd
import plotly_express as px

# Create your charts here 
df = pd.read_csv("Data/athlete_events.csv") 

def select_sport(selection_of_sport):
    chosen_sport = (df["Sport"] == selection_of_sport) & (df["Medal"].notna())
    medals_by_country = (df[chosen_sport].groupby("NOC")[["Medal"]].count().sort_values(by="Medal",ascending=False).reset_index()) # groups by NOC and counts number of medals, sort values and then resets index.
    return medals_by_country

# Add your completed charts to the select dictionary
# check the tobbe.py file for reference
select={
        "Sailing": px.bar(
            select_sport("Sailing"),
            x="NOC",
            y="Medal",
            color="NOC",
            title= f"Medal overview in Sailing"
         ),
        "Canoeing": px.bar(
            select_sport("Canoeing"),
            x="NOC",
            y="Medal",
            color="NOC",
            title= f"Medal overview in Canoeing"
         ),

}