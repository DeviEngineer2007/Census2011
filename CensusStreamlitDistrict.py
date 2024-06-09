import streamlit as st
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import plotly.express as px

# Database connection parameters
db_name = 'test1'
db_user = 'root'
db_password = ''
db_host = 'localhost'

# Use SQLAlchemy to create engine
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

# Function to load the entire dataset into a DataFrame
@st.cache_data(ttl=600)  # Cache the data to improve performance
def load_data():
    query = "SELECT * FROM census"
    return pd.read_sql(query, engine)

# Load the dataset
df = load_data()

# Streamlit app
st.title("Census Data Analysis Dashboard")

# User selects the state
states = df['StateUT'].unique()
selected_state = st.selectbox("Select a state to visualize:", ["All States"] + list(states))

# Filter the data by the selected state
if selected_state != "All States":
    df = df[df['StateUT'] == selected_state]

# User selects the query
query_options = [
    "Total Population by District",
    "Literate Males and Females by District",
    "Workers Percentage by District",
    "Households with LPG or PNG by District",
    "Religious Composition by District",
    "Households with Internet Access by District",
    "Educational Attainment by District",
    "Households with Various Modes of Transportation by District",
    "Condition of Occupied Census Houses by District",
    "Household Size Distribution by District"
     
]
query_selection = st.selectbox("Select a query to visualize:", query_options)

# Process the selected query using Pandas
if query_selection == "Total Population by District":
    df_result = df.groupby("District").agg({"Population": "sum"}).reset_index()
    df_result.rename(columns={"Population": "Total_Population"}, inplace=True)
    fig = px.bar(df_result, x='District', y='Total_Population', title='Total Population by District')

elif query_selection == "Literate Males and Females by District":
    df_result = df.groupby("District").agg({"Literate_Male": "sum", "Literate_Female": "sum"}).reset_index()
    fig = px.bar(df_result, x='District', y=['Literate_Male', 'Literate_Female'], title="Literate Males and Females by District")

elif query_selection == "Workers Percentage by District":
    df_result = df.groupby("District").agg({"Male_Workers": "sum", "Female_Workers": "sum", "Population": "sum"}).reset_index()
    df_result["Workers_Percentage"] = (df_result["Male_Workers"] + df_result["Female_Workers"]) / df_result["Population"] * 100
    fig = px.pie(df_result, names='District', values='Workers_Percentage', title="Workers Percentage by District")

elif query_selection == "Households with LPG or PNG by District":
    df_result = df.groupby("District").agg({"Households_with_LPG_PNG": "sum"}).reset_index()
    fig = px.pie(df_result, names='District', values='Households_with_LPG_PNG', title="Households with LPG or PNG by District")

elif query_selection == "Religious Composition by District":
    df_result = df.groupby("District").agg({"Hindus": "sum", "Muslims": "sum", "Christians": "sum", "Others": "sum"}).reset_index()
    fig = px.bar(df_result, x='District', y=['Hindus', 'Muslims', 'Christians', 'Others'], title="Religious Composition by District")

elif query_selection == "Households with Internet Access by District":
    df_result = df.groupby("District").agg({"Households_with_Internet": "sum"}).reset_index()
    fig = px.bar(df_result, x='District', y='Households_with_Internet', title="Households with Internet Access by District")

elif query_selection == "Educational Attainment by District":
    df_result = df.groupby("District").agg({
        "Below_Primary_Education": "sum",
        "Primary_Education": "sum",
        "Middle_Education": "sum",
        "Secondary_Education": "sum",
        "Higher_Education": "sum",
        "Graduate_Education": "sum",
        "Other_Education": "sum"
    }).reset_index()
    df_melted = df_result.melt(id_vars=["District"], var_name="Education_Level", value_name="Count")
    fig = px.bar(df_melted, x="District", y="Count", color="Education_Level", title="Educational Attainment by District", barmode='stack')

elif query_selection == "Households with Various Modes of Transportation by District":
    df_result = df.groupby("District").agg({
        "Households_with_Bicycle": "sum",
        "Households_with_Car_Jeep_Van": "sum",
        "Households_with_Radio_Transistor": "sum",
        "Households_with_Television": "sum"
    }).reset_index()
    fig = px.bar(df_result, x='District', y=['Households_with_Bicycle', 'Households_with_Car_Jeep_Van', 'Households_with_Radio_Transistor', 'Households_with_Television'], title="Households with Various Modes of Transportation by District")

elif query_selection == "Condition of Occupied Census Houses by District":
    df_result = df.groupby("District").agg({
        "Condition_of_occupied_census_houses_Dilapidated_Households": "sum",
        "Houses_with_Separate_Kitchen": "sum",
        "Having_bathing_facility_Total_Households": "sum",
        "Houses_with_Latrine_Facility": "sum"
    }).reset_index()
    fig = px.bar(df_result, x='District', y=['Condition_of_occupied_census_houses_Dilapidated_Households', 'Houses_with_Separate_Kitchen', 'Having_bathing_facility_Total_Households', 'Houses_with_Latrine_Facility'], title="Condition of Occupied Census Houses by District")

elif query_selection == "Household Size Distribution by District":
    df_result = df.groupby("District").agg({
        "Household_size_1_person": "sum",
        "Household_size_2_persons": "sum",
        "Household_size_3_to_5_persons": "sum",
        "Household_size_6_8_persons": "sum",
        "Household_size_9_or_more_persons": "sum"
    }).reset_index()
    fig = px.bar(df_result, x='District', y=['Household_size_1_person', 'Household_size_2_persons', 'Household_size_3_to_5_persons', 'Household_size_6_8_persons', 'Household_size_9_or_more_persons'], title="Household Size Distribution by District")

    
 

# Display the chart
st.plotly_chart(fig)