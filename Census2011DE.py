from docx import Document;
import openpyxl
import io;
import pandas as pd;
import re;
import numpy as np
from pymongo import MongoClient
import mysql.connector
from sqlalchemy import create_engine

##################################################TASK 1 BEGIN###########################################################################
# Read the Excel file and store it into a DataFrame
pathname = "C:\\Users\\Senthil\\Desktop\\GuviPracticeClass\\GuviCapstoneproject\\census_2011.xlsx"
data = pd.read_excel(pathname)

# Keep a copy of the original data
data_before = data.copy()
print("Before Modification:")
print(list(data.columns))
# Function implementation for renaming the columns
def rename_function(datatorename):
    # Store the data frame with modified column names
     renameddata = datatorename.rename(columns={\
    'District code':'District_code','State name':'StateUT','District name':'District',\
    'Male_Literate':'Literate_Male','Female_Literate':'Literate_Female','Rural_Households':'Households_Rural',\
    'Urban_Households':'Households_Urban','LPG_or_PNG_Households':'Households_with_LPG_PNG',\
    'Having_latrine_facility_within_the_premises_Total_Households':'Houses_with_Latrine_Facility',\
    'Households_with_separate_kitchen_Cooking_inside_house':'Houses_with_Separate_Kitchen',\
    'Others_Religions':'Others','Household_size_1_person_Households':'Household_size_1_person',\
    'Household_size_2_persons_Households':'Household_size_2_persons','Household_size_3_persons_Households':'Household_size_3_persons',\
    'Household_size_3_to_5_persons_Households':'Household_size_3_to_5_persons', 'Household_size_4_persons_Households':'Household_size_4_persons',\
    'Household_size_5_persons_Households':'Household_size_5_persons', 'Household_size_6_8_persons_Households':'Household_size_6_8_persons',\
    'Household_size_9_persons_and_above_Households':'Household_size_9_or_more_persons', 'Age_Group_0_29':'Young_and_Adult',\
    'Age_Group_30_49':'Middle_Aged','Age_Group_50':'Senior_Citizen',\
    'Households_with_TV_Computer_Laptop_Telephone_mobile_phone_and_Scooter_Car': 'Households_with_TV_Comp_Laptop_Phone_and_Vehicle',\
    'Type_of_latrine_facility_Night_soil_disposed_into_open_drain_Households': 'Latrine_facility_Night_soil_open_drain_Households',\
    'Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_other_system_Households': 'Latrine_Flush_connected_to_system_Households',\
    'Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households': 'No_latrine_Alternative_source_Open_Households',\
    'Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households': 'Main_drinking_water_Handpump_Tubewell_Borewell_Households',\
    'Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households': \
    'Main_drinking_water_Other_sources_Households',\
    'Age not stated':'Age_Not_Stated'})
     return renameddata  # Return the modified DataFrame

# Calling the rename function, passing the DataFrame 'data' as argument
data = rename_function(data)
data_after=data
# Print the DataFrame to verify changes (optional)
modified_columns=[
    'District code','State name','District name', 'Male_Literate','Female_Literate','Rural_Households',
    'Urban_Households','LPG_or_PNG_Households','Having_latrine_facility_within_the_premises_Total_Households',
    'Households_with_separate_kitchen_Cooking_inside_house','Others_Religions','Household_size_1_person_Households',
    'Household_size_2_persons_Households','Household_size_3_persons_Households','Household_size_3_to_5_persons_Households',
    'Household_size_4_persons_Households','Household_size_5_persons_Households',
    'Household_size_6_8_persons_Households','Household_size_9_persons_and_above_Households','Age_Group_0_29',
    'Age_Group_30_49','Age_Group_50','Households_with_TV_Computer_Laptop_Telephone_mobile_phone_and_Scooter_Car',
    'Type_of_latrine_facility_Night_soil_disposed_into_open_drain_Households', 'Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_other_system_Households',
    'Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households',
    'Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households',
    'Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households',
    'Age not stated']
print("Modified Columns Before and After:")
column_names = {'Before': [], 'After': []}
for col in modified_columns:
    old_name = col
    new_name = rename_function(pd.DataFrame({col: []})).columns[0]
    column_names['Before'].append(old_name)
    column_names['After'].append(new_name)
    # Convert the dictionary to a DataFrame
column_names_df = pd.DataFrame(column_names)

# Print the DataFrame showing old and new column names
def print_rename():
    global column_names_df 
    print("Old and New Column Names:")
    print(column_names_df)
##################################################TASK 1 completed###########################################################################

####################################################TASK 2 BEGIN#############################################################################

# Function to standardize state names by capitalizing each word except 'AND' and 'OF'
def standardize_state_names(name):
    # Split the state name into individual words
    words = name.split()
    # Capitalize each word unless it is 'AND' or 'OF'
    standardized_words = [word.capitalize() if word not in ['AND', 'OF'] else word.lower() for word in words]
    # Join the words back into a single string with spaces in between
    return ' '.join(standardized_words)
# Apply the standardize_state_names function to each element in the 'StateUT' column of the DataFrame
data['StateUT'] = data['StateUT'].apply(standardize_state_names)
# Print the DataFrame to see the standardized state names
def print_stand_name():
 global data
 print(data)
##################################################TASK 2 completed###########################################################################

####################################################TASK 3 BEGIN#############################################################################
from docx import Document

# Define the path to the Word document
doc_path = 'C:\\Users\\Senthil\\Desktop\\GuviPracticeClass\\GuviCapstoneproject\\Telangana.docx'

# Load the Word document
document = Document(doc_path)

# Extract text from paragraphs using a set comprehension to remove duplicates and strip whitespace
districts = {p.text.strip() for p in document.paragraphs if p.text.strip()}

# Update the 'StateUT' column to 'Telangana' for rows where 'District' is in the extracted districts
data.loc[data['District'].isin(districts), 'StateUT'] = 'Telangana'

# Define the districts for Ladakh
ladakh_districts = ['Leh(Ladakh)', 'Kargil']

# Update the 'StateUT' column to 'Ladakh' for rows where 'District' is in the Ladakh districts
data.loc[data['District'].isin(ladakh_districts), 'StateUT'] = 'Ladakh'
def print_new_state_name():
  global data
  print(data)
##################################################TASK 3 completed###########################################################################

##################################################TASK 4 BEGIN###############################################################################

import pandas as pd

# Calculate and print the initial percentage of missing values for each column
missing_percentages_initial = data.isnull().mean() * 100
print("Initial missing percentages:\n", missing_percentages_initial)

# Function to fill missing values in the DataFrame
def fill_missing_values(df):
    # Fill 'Population' with the sum of 'Male' and 'Female'
    df['Population'] = df['Population'].fillna(df['Male'] + df['Female'])
    
    # Fill 'Literate' with the sum of 'Literate_Male' and 'Literate_Female'
    df['Literate'] = df['Literate'].fillna(df['Literate_Male'] + df['Literate_Female'])
    
    # Fill 'Households' with the sum of 'Households_Rural' and 'Households_Urban'
    df['Households'] = df['Households'].fillna(df['Households_Rural'] + df['Households_Urban'])
    
    # Alternative way to fill 'Population' with the sum of age groups
    df['Population'] = df['Population'].fillna(df['Young_and_Adult'] + df['Middle_Aged'] + df['Senior_Citizen'] + df['Age_Not_Stated'])
    
    # Fill 'SC' with the sum of 'Male_SC' and 'Female_SC'
    df['SC'] = df['SC'].fillna(df['Male_SC'] + df['Female_SC'])
    
    # Fill 'ST' with the sum of 'Male_ST' and 'Female_ST'
    df['ST'] = df['ST'].fillna(df['Male_ST'] + df['Female_ST'])
    
    # Fill 'Workers' with the sum of 'Male_Workers' and 'Female_Workers'
    df['Workers'] = df['Workers'].fillna(df['Male_Workers'] + df['Female_Workers'])
    
    # Fill 'Non_Workers' by subtracting 'Workers' from 'Population'
    df['Non_Workers'] = df['Non_Workers'].fillna(df['Population'] - df['Workers'])
    
    # Alternative way to fill 'Workers' with the sum of 'Main_Workers' and 'Marginal_Workers'
    df['Workers'] = df['Workers'].fillna(df['Main_Workers'] + df['Marginal_Workers'])
    
    # Fill 'Literate_Male' by subtracting 'Literate_Female' from 'Literate'
    df['Literate_Male'] = df['Literate_Male'].fillna(df['Literate'] - df['Literate_Female'])
    
    # Fill 'Literate_Female' by subtracting 'Literate_Male' from 'Literate'
    df['Literate_Female'] = df['Literate_Female'].fillna(df['Literate'] - df['Literate_Male'])
    
    # Fill 'Cultivator_Workers' by subtracting other types of workers from 'Workers'
    df['Cultivator_Workers'] = df['Cultivator_Workers'].fillna(df['Workers'] - df['Agricultural_Workers'] - df['Household_Workers'] - df['Other_Workers'])
    
    # Fill 'Agricultural_Workers' by subtracting other types of workers from 'Workers'
    df['Agricultural_Workers'] = df['Agricultural_Workers'].fillna(df['Workers'] - df['Cultivator_Workers'] - df['Household_Workers'] - df['Other_Workers'])
    
    # Fill 'Household_Workers' by subtracting other types of workers from 'Workers'
    df['Household_Workers'] = df['Household_Workers'].fillna(df['Workers'] - df['Cultivator_Workers'] - df['Agricultural_Workers'] - df['Other_Workers'])
    
    # Fill 'Other_Workers' by subtracting other types of workers from 'Workers'
    df['Other_Workers'] = df['Other_Workers'].fillna(df['Workers'] - df['Cultivator_Workers'] - df['Agricultural_Workers'] - df['Household_Workers'])
    
    # Fill 'Total_Education' with the sum of various education levels
    df['Total_Education'] = df['Below_Primary_Education'] + df['Primary_Education'] + df['Middle_Education'] + df['Secondary_Education'] + df['Higher_Education'] + df['Graduate_Education'] + df['Other_Education'] + df['Literate_Education'] + df['Illiterate_Education']
    
    # Fill 'Location_of_drinking_water_source_Total' with the sum of different water source locations
    df['Location_of_drinking_water_source_Total'] = df['Location_of_drinking_water_source_Near_the_premises_Households'] + df['Location_of_drinking_water_source_Within_the_premises_Households'] + df['Location_of_drinking_water_source_Away_Households']
    
    # Fill 'Household_size_Total' with the sum of various household sizes
    df['Household_size_Total'] = df['Household_size_1_person'] + df['Household_size_2_persons'] + df['Household_size_3_persons'] + df['Household_size_4_persons'] + df['Household_size_5_persons'] + df['Household_size_6_8_persons'] + df['Household_size_9_or_more_persons']
    
    # Fill 'Total_Power_Parity' with the sum of different power parity categories
    df['Total_Power_Parity'] = df['Power_Parity_Less_than_Rs_45000'] + df['Power_Parity_Rs_45000_90000'] + df['Power_Parity_Rs_90000_150000'] + df['Power_Parity_Rs_150000_240000'] + df['Power_Parity_Rs_240000_330000'] + df['Power_Parity_Rs_330000_425000'] + df['Power_Parity_Rs_425000_545000'] + df['Power_Parity_Above_Rs_545000']
    
    return df

# Apply the filling logic to the DataFrame
data_filled = fill_missing_values(data)

# Calculate and print the percentage of missing values after filling
missing_percentages_final = data_filled.isnull().mean() * 100
print("Final missing percentages:\n", missing_percentages_final)

# Update the original DataFrame with the filled data
data = data_filled

# Compare the missing data percentages before and after filling
comparison = pd.DataFrame({
    'Initial': missing_percentages_initial,
    'Final': missing_percentages_final
})
def print_comparison():
 global comparison
 global data
 print("Comparison of missing percentages:\n", comparison)
 print(data.columns.tolist())

# Optional: Save missing data comparison to a CSV file for reporting
# comparison.to_csv('missing_data_comparison.csv', index=True)
##################################################TASK 4 completed###########################################################################

####################################################TASK 5 BEGIN#############################################################################

# Step 1: Define the MongoDB connection URI
uri = "mongodb+srv://devisenthilkumar2024:tamil@cluster0.lzkkk4j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Step 2: Connect to the MongoDB cluster
client = MongoClient(uri)
collection = client.testdb.collection3

# Step 3: Convert the DataFrame to a list of dictionaries
data_dict = data.to_dict(orient='records')

# Step 4: Upsert the data into the MongoDB collection
for record in data_dict:
    # Using a composite key of 'Population' and 'DistrictName' to avoid duplicates
    collection.update_one(
        {'Population': record['Population'], 'District': record['District']},
        {'$set': record},
        upsert=True
    )

# Step 5: Print a success message to confirm data insertion
def print_Mongo():
 global data
 print("Data inserted successfully into MongoDB")
 print(data.columns.tolist())

###################################################TASK 5 completed###########################################################################

##################################################TASK  6 BEGIN##############################################################################
 
# Step 2: Connect to the MongoDB cluster
#client = MongoClient(uri)
#collection = client.testdb.collection3

# Fetch the data
data1 = list(collection.find())

# Step 1: Fetch data from MongoDB
# Convert the MongoDB cursor object to a list of dictionaries
#data = list(client.find())

# Step 2: Convert the list of dictionaries to a pandas DataFrame
data_df = pd.DataFrame(data1)

# Step 3: Drop the MongoDB specific '_id' column if it exists
# This column is auto-generated by MongoDB and not required in MySQL
if '_id' in data_df.columns:
    data_df = data_df.drop('_id', axis=1)

# Database connection details for MySQL
db_name = 'test1'
db_user = 'root'
db_password = ''
db_host = 'localhost'

# Step 4: Create a connection to MySQL using mysql.connector
connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

# Step 5: Use SQLAlchemy to create an engine for MySQL
# This engine is used to interact with the MySQL database
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

# Step 6: Retrieve column names from the DataFrame
columns = data_df.columns

 

# Step 7: Define the data types for the columns
# 'INT AUTO_INCREMENT PRIMARY KEY' is used for the first column (assumed to be an ID column)
# 'VARCHAR(255)' is used for the next two columns (assumed to be string data)
# 'INT' is used for the remaining columns (assumed to be numeric data)
data_types = ['INT AUTO_INCREMENT PRIMARY KEY'] + ['VARCHAR(255)'] * 2 + ['INT'] * (len(columns) - 3)

# Step 8: Create a SQL statement to create the table in MySQL
create_table_query = "CREATE TABLE IF NOT EXISTS census1 ("
for column, data_type in zip(columns, data_types):
    create_table_query += f"{column} {data_type}, "
create_table_query = create_table_query.rstrip(", ") + ");"

# Print the create table query for verification
#print("Create table query:")
#print(create_table_query)

# Step 9: Execute the create table query
# This creates the 'census' table in the MySQL database if it does not already exist
with connection.cursor() as cursor:
    cursor.execute(create_table_query)
    connection.commit()

# Step 10: Insert data into the MySQL table using pandas to_sql method
# This method replaces any existing data in the 'census' table
data_df.to_sql('census1', con=engine, if_exists='replace', index=False)

def print_Sql():
# Step 11: Print a success message to confirm data insertion
  print("Data inserted successfully into MySQL")

# Print the data again for final verification
  print(data.columns.tolist()) 
  print(data_df.columns.tolist())
##################################################TASK 6 completed###########################################################################

print(f"Below are the tasks names which can be performed : \
      \n 1. Rename Function \
      \n 2. Standardizing State Names\
      \n 3. Handling Missing Values\
      \n 4. Mapping District to state\
      \n 5. Storing Data in MongoDB\
      \n 6. Transferring Data from MongoDB to MySQL\
    \n 0.Exit")

tasknumber =input("Please select the Task number:")

if tasknumber == '1':
    print_rename()

elif tasknumber == '2':
    print_stand_name()
elif tasknumber == '3':
    print_new_state_name
elif tasknumber == '4':
    print_comparison
elif tasknumber == '5':
    print_Mongo()
elif tasknumber == '6':
    print_Sql()
else:
    print("Wrong option")

