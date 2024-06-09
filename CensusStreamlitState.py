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

 

# User selects the query
query_options = [
     
    "Total Households by State",
    "Households with Latrine Facility by State",
    "Average Household Size by State",
    "Owned vs Rented Households by State",
    "Types of Latrine Facilities by State",
    "Households with Drinking Water Sources by State",
    "Household Income Distribution by State",
    "Married Couples with Different Household Sizes by State",
    "Households Below the Poverty Line by State",
    "Overall Literacy Rate by State"
]
query_selection = st.selectbox("Select a query to visualize:", query_options)

if query_selection == "Total Households by State":
    df_result = df.groupby("StateUT").agg({"Households": "sum"}).reset_index()
    df_result.rename(columns={"Households": "Total_Households"}, inplace=True)
    fig = px.bar(df_result, x='StateUT', y='Total_Households', title='Total Households by State')

elif query_selection == "Households with Latrine Facility by State":
    df_result = df.groupby("StateUT").agg({"Houses_with_Latrine_Facility": "sum"}).reset_index()
    fig = px.bar(df_result, x='StateUT', y='Houses_with_Latrine_Facility', title='Houses with Latrine Facility by State')

elif query_selection == "Average Household Size by State":
    df_result = df.groupby("StateUT").agg({"Household_size_Total": "mean"}).reset_index()
    df_result.rename(columns={"Household_size_Total": "Average_Household_Size"}, inplace=True)
    fig = px.bar(df_result, x='StateUT', y='Average_Household_Size', title='Average Household Size by State')

elif query_selection == "Owned vs Rented Households by State":
    df_result = df.groupby("StateUT").agg({"Ownership_Owned_Households": "sum", "Ownership_Rented_Households": "sum"}).reset_index()
    fig = px.bar(df_result, x='StateUT', y=['Ownership_Owned_Households', 'Ownership_Rented_Households'], title='Owned vs Rented Households by State')

elif query_selection == "Types of Latrine Facilities by State":
    df_result = df.groupby("StateUT").agg({"Latrine_facility_Night_soil_open_drain_Households": "sum", "Latrine_Flush_connected_to_system_Households": "sum", "Type_of_latrine_facility_Other_latrine_Households": "sum","Type_of_latrine_facility_Pit_latrine_Households": "sum"}).reset_index()
    fig = px.bar(df_result, x='StateUT', y=['Latrine_facility_Night_soil_open_drain_Households', 'Latrine_Flush_connected_to_system_Households', 'Type_of_latrine_facility_Other_latrine_Households','Type_of_latrine_facility_Pit_latrine_Households'], title='Types of Latrine Facilities by State')

elif query_selection == "Households with Drinking Water Sources by State":
    df_result = df.groupby("StateUT").agg({"Location_of_drinking_water_source_Near_the_premises_Households": "sum"}).reset_index()
    fig = px.bar(df_result, x='StateUT', y='Location_of_drinking_water_source_Near_the_premises_Households', title="Households with Drinking Water Sources by State")

elif query_selection == "Household Income Distribution by State":
    df_result = df.groupby("StateUT").agg({
        "Income_Below_Poverty_Line": "sum",
        "Income_Low": "sum",
        "Income_Middle": "sum",
        "Income_High": "sum"
    }).reset_index()
    df_melted = df_result.melt(id_vars=["StateUT"], var_name="Income_Level", value_name="Count")
    fig = px.bar(df_melted, x="StateUT", y="Count", color="Income_Level", title="Household Income Distribution by State", barmode='stack')

elif query_selection == "Married Couples with Different Household Sizes by State":
    df_result = df.groupby("StateUT").agg({
        "Couples_Household_size_1": "sum",
        "Couples_Household_size_2": "sum",
        "Couples_Household_size_3_5": "sum",
        "Couples_Household_size_6_8": "sum",
        "Couples_Household_size_9_or_more": "sum"
    }).reset_index()
    fig = px.bar(df_result, x='StateUT', y=['Couples_Household_size_1', 'Couples_Household_size_2', 'Couples_Household_size_3_5', 'Couples_Household_size_6_8', 'Couples_Household_size_9_or_more'], title="Married Couples with Different Household Sizes by State")

elif query_selection == "Households Below the Poverty Line by State":
    df_result = df.groupby("StateUT").agg({"Households_Below_Poverty_Line": "sum"}).reset_index()
    fig = px.bar(df_result, x='StateUT', y='Households_Below_Poverty_Line', title='Households Below the Poverty Line by State')

elif query_selection == "Overall Literacy Rate by State":
    df_result = df.groupby("StateUT").agg({
        "Literate_Male": "sum",
        "Literate_Female": "sum",
        "Population": "sum"
    }).reset_index()
    df_result["Literacy_Rate"] = (df_result["Literate_Male"] + df_result["Literate_Female"]) / df_result["Population"] * 100
    fig = px.bar(df_result, x='StateUT', y='Literacy_Rate', title='Overall Literacy Rate by State')

# Display the chart
st.plotly_chart(fig)
 