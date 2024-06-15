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
pathname = "C:\\Users\\Senthil\\Desktop\\Census2011CapstoneProject\\census_2011.xlsx"
data = pd.read_excel(pathname)
# Keep a copy of the original data
data_before_rename = data.copy()
# Function implementation for renaming the columns
def rename_function(dataframe_to_rename):
        # Read the Excel file with the column mappings
        column_mappings_df = pd.read_excel("C:\\Users\\Senthil\\Desktop\\Census2011CapstoneProject\\col_name.xlsx")
        # Convert the mappings to a dictionary
        column_mappings = dict(zip(column_mappings_df['OldName'], column_mappings_df['NewName']))
        # Rename the columns
        renamed_data = dataframe_to_rename.rename(columns=column_mappings)
        return  renamed_data
# Calling the rename function, passing the DataFrame 'data' as argument
data = rename_function(data_before_rename)

data.to_excel('rename_data.xlsx', index=True)
data_after_rename=data
 # Print the DataFrame showing old and new column names
def print_rename():
    pr=pd.DataFrame({'Before:':data_before_rename.columns.to_list(),'After:':data_after_rename.columns.to_list()})
    print(pr)
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
def standardize_district_names(name):
    # Split the state name into individual words based on spaces, parentheses, and hyphens
    words = re.split(r'([\s\(\)\-]+)', name)
     
    # Capitalize words that are not in the exclusion list ('and') or are not special characters
    standardized_words = [
        word.lower() if word.lower() in ['and'] and word[0].isalpha() else word.capitalize()
        for word in words
    ]
    # Join the words back into a single string with the original separators
    standardized_name = ''.join(standardized_words)
    
    return standardized_name.strip()  # Strip leading and trailing spaces

# Apply the standardize_state_names function to each element in the 'StateUT' column of the DataFrame
data['StateUT'] = data['StateUT'].apply(standardize_state_names)
# Standardize the 'District' column
data['District'] = data['District'].apply(standardize_district_names)
# writing data from DataFrame to Excel
data.to_excel('standard_name_data.xlsx', index=True)
# Print the DataFrame to see the standardized state names
def print_stand_name():
 global data
 print(data['StateUT'].unique())
 #print(data['District'].values)

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
  print(data.iloc[:,1:3])
 ##################################################TASK 3 completed###########################################################################

##################################################TASK 4 BEGIN###############################################################################

# Calculate and print the initial percentage of missing values for each column
missing_percentages_initial = data.isnull().mean() * 100
print("Initial missing percentages:\n", missing_percentages_initial)

# Function to fill missing values in the DataFrame
def fill_missing_values(df):
        # Fill 'Population' with the sum of 'Male' and 'Female'
    df['Population'] = df['Population'].fillna(df['Male'] + df['Female'])
    df['Population'] = df['Population'].fillna(df['Main_Workers'] + df['Marginal_Workers'] + df['Non_Workers'])
    df['Male'] = df['Male'].fillna(df['Population'] - df['Female'])
    df['Female'] = df['Female'].fillna(df['Population'] - df['Male'])
    df['Young_and_Adult'] = df['Young_and_Adult'].fillna(df['Population'] - (df['Senior_Citizen'] + df['Middle_Aged'] + df['Age_Not_Stated']))
    df['Middle_Aged'] = df['Middle_Aged'].fillna(df['Population'] - (df['Young_and_Adult'] + df['Senior_Citizen'] + df['Age_Not_Stated']))
    df['Senior_Citizen'] = df['Senior_Citizen'].fillna(df['Population'] - (df['Young_and_Adult'] + df['Middle_Aged'] + df['Age_Not_Stated']))
    df['Age_Not_Stated'] = df['Age_Not_Stated'].fillna(df['Population'] - (df['Young_and_Adult'] + df['Middle_Aged'] + df['Senior_Citizen']))
    df['Population'] = df['Population'].fillna(df['Young_and_Adult'] + df['Middle_Aged'] + df['Senior_Citizen'] + df['Age_Not_Stated'])

# Fill 'Literate' with the sum of 'Literate_Male' and 'Literate_Female'
    df['Literate'] = df['Literate'].fillna(df['Literate_Male'] + df['Literate_Female'])
    df['Literate_Male'] = df['Literate_Male'].fillna(df['Literate'] - df['Literate_Female'])
    df['Literate_Female'] = df['Literate_Female'].fillna(df['Literate'] - df['Literate_Male'])

# Fill 'Households' with the sum of 'Households_Rural' and 'Households_Urban'
    df['Households'] = df['Households'].fillna(df['Households_Rural'] + df['Households_Urban'])
    df['Households_Rural'] = df['Households_Rural'].fillna(df['Households'] - df['Households_Urban'])
    df['Households_Urban'] = df['Households_Urban'].fillna(df['Households'] - df['Households_Rural'])

# Fill 'SC' with the sum of 'Male_SC' and 'Female_SC'
    df['SC'] = df['SC'].fillna(df['Male_SC'] + df['Female_SC'])
    df['Male_SC'] = df['SC'].fillna(df['SC'] - df['Female_SC'])
    df['Female_SC'] = df['SC'].fillna(df['SC'] - df['Male_SC'])

# Fill 'ST' with the sum of 'Male_ST' and 'Female_ST'
    df['ST'] = df['ST'].fillna(df['Male_ST'] + df['Female_ST'])
    df['Male_ST'] = df['ST'].fillna(df['ST'] - df['Female_ST'])
    df['Female_ST'] = df['ST'].fillna(df['ST'] - df['Male_ST'])
# Fill 'Workers' with the sum of 'Male_Workers' and 'Female_Workers'
    df['Workers'] = df['Workers'].fillna(df['Male_Workers'] + df['Female_Workers'])
    df['Male_Workers'] = df['Male_Workers'].fillna(df['Workers'] - df['Female_Workers'])
    df['Female_Workers'] = df['Female_Workers'].fillna(df['Workers']- df['Male_Workers'])

    df['Workers'] = df['Workers'].fillna(df['Main_Workers'] + df['Marginal_Workers'])
    df['Main_Workers']  = df['Main_Workers'] .fillna( df['Workers'] - df['Marginal_Workers'])

    df['Marginal_Workers']= df['Marginal_Workers'].fillna( df['Workers'] - df['Main_Workers'] )
    df['Non_Workers'] = df['Non_Workers'].fillna(df['Population'] - df['Workers'])
    df['Workers'] = df['Workers'].fillna(df['Population'] - df['Non_Workers'])
# Fill 'Cultivator_Workers' by subtracting other types of workers from 'Workers'
    df['Cultivator_Workers'] = df['Cultivator_Workers'].fillna(df['Workers'] - df['Agricultural_Workers'] - df['Household_Workers'] - df['Other_Workers'])

# Fill 'Agricultural_Workers' by subtracting other types of workers from 'Workers'
    df['Agricultural_Workers'] = df['Agricultural_Workers'].fillna(df['Workers'] - df['Cultivator_Workers'] - df['Household_Workers'] - df['Other_Workers'])
# Fill 'Household_Workers' by subtracting other types of workers from 'Workers'
    df['Household_Workers'] = df['Household_Workers'].fillna(df['Workers'] - df['Cultivator_Workers'] - df['Agricultural_Workers'] - df['Other_Workers'])
# Fill 'Other_Workers' by subtracting other types of workers from 'Workers'
    df['Other_Workers'] = df['Other_Workers'].fillna(df['Workers'] - df['Cultivator_Workers'] - df['Agricultural_Workers'] - df['Household_Workers'])

# Fill 'Total_Education' with the sum of various education levels
    df['Total_Education'] = df['Total_Education'].fillna(
    df['Below_Primary_Education'] + df['Primary_Education'] + df['Middle_Education'] + 
    df['Secondary_Education'] + df['Higher_Education'] + df['Graduate_Education'] + 
    df['Other_Education'] + df['Literate_Education'] + df['Illiterate_Education'])



# Fill 'Total_Power_Parity' with the sum of different power parity categories 	
    df['Power_Parity_Rs_45000_150000'] =df['Power_Parity_Rs_45000_150000'].fillna(df['Power_Parity_Rs_45000_90000']	+   df['Power_Parity_Rs_90000_150000'])
    df['Power_Parity_Rs_45000_90000'] = df['Power_Parity_Rs_45000_90000'].fillna(df['Power_Parity_Rs_45000_150000']-df['Power_Parity_Rs_45000_90000'])
    df['Power_Parity_Rs_90000_150000'] =df['Power_Parity_Rs_90000_150000'].fillna(df['Power_Parity_Rs_45000_150000'] -df['Power_Parity_Rs_90000_150000'])
    df['Power_Parity_Rs_150000_330000'] = df['Power_Parity_Rs_150000_330000'].fillna( df['Power_Parity_Rs_150000_240000'] + df['Power_Parity_Rs_240000_330000'])

# Fill missing values for 'Power_Parity_Rs_150000_240000' 
    df['Power_Parity_Rs_150000_240000'] = df['Power_Parity_Rs_150000_240000'].fillna(df['Power_Parity_Rs_150000_330000'] - df['Power_Parity_Rs_240000_330000'])
# Fill missing values for 'Power_Parity_Rs_240000_330000'
    df['Power_Parity_Rs_240000_330000'] = df['Power_Parity_Rs_240000_330000'].fillna(df['Power_Parity_Rs_150000_330000'] - df['Power_Parity_Rs_150000_240000'])
    

    df['Power_Parity_Rs_330000_545000']=df['Power_Parity_Rs_330000_545000'].fillna(df['Power_Parity_Rs_330000_425000']+df['Power_Parity_Rs_425000_545000'])
    df['Power_Parity_Rs_330000_425000']=df['Power_Parity_Rs_330000_425000'].fillna(df['Power_Parity_Rs_330000_545000']-df['Power_Parity_Rs_425000_545000'])
    df['Power_Parity_Rs_425000_545000']=df['Power_Parity_Rs_425000_545000'].fillna(df['Power_Parity_Rs_330000_545000']-df['Power_Parity_Rs_330000_425000'])
    df['Total_Power_Parity'] = df['Total_Power_Parity'].fillna(
    df['Power_Parity_Less_than_Rs_45000'] + df['Power_Parity_Rs_45000_90000'] + df['Power_Parity_Rs_90000_150000'] + 
    df['Power_Parity_Rs_150000_330000'] + df['Power_Parity_Rs_330000_425000'] + 
    df['Power_Parity_Rs_425000_545000'] + df['Power_Parity_Above_Rs_545000']) 

    df['Power_Parity_Less_than_Rs_45000'] =df['Power_Parity_Less_than_Rs_45000'].fillna(df['Total_Power_Parity']-df['Power_Parity_Rs_45000_90000'] + df['Power_Parity_Rs_90000_150000'] + 
    df['Power_Parity_Rs_150000_330000'] + df['Power_Parity_Rs_330000_425000'] + 
    df['Power_Parity_Rs_425000_545000'] + df['Power_Parity_Above_Rs_545000'])
    df['Power_Parity_Rs_45000_90000'] =df['Power_Parity_Rs_45000_90000'] .fillna(df['Power_Parity_Less_than_Rs_45000'] + df['Power_Parity_Rs_90000_150000'] + 
    df['Power_Parity_Rs_150000_330000'] + df['Power_Parity_Rs_330000_425000'] + 
    df['Power_Parity_Rs_425000_545000'] + df['Power_Parity_Above_Rs_545000']) 
    df['Power_Parity_Rs_90000_150000']=df['Power_Parity_Rs_90000_150000'].fillna(df['Power_Parity_Less_than_Rs_45000'] + df['Power_Parity_Rs_45000_90000']  + 
    df['Power_Parity_Rs_150000_330000'] + df['Power_Parity_Rs_330000_425000'] + 
    df['Power_Parity_Rs_425000_545000'] + df['Power_Parity_Above_Rs_545000']) 
    df['Power_Parity_Rs_150000_330000']= df['Power_Parity_Rs_150000_330000'].fillna(df['Power_Parity_Less_than_Rs_45000'] + df['Power_Parity_Rs_45000_90000'] + df['Power_Parity_Rs_90000_150000'] + 
     + df['Power_Parity_Rs_330000_425000'] + 
    df['Power_Parity_Rs_425000_545000'] + df['Power_Parity_Above_Rs_545000']) 
    df['Power_Parity_Rs_330000_425000']= df['Power_Parity_Rs_330000_425000'].fillna(df['Power_Parity_Less_than_Rs_45000'] + df['Power_Parity_Rs_45000_90000'] + df['Power_Parity_Rs_90000_150000'] + 
    df['Power_Parity_Rs_150000_330000']  + df['Power_Parity_Rs_425000_545000'] + df['Power_Parity_Above_Rs_545000']) 
    df['Power_Parity_Rs_425000_545000'] =  df['Power_Parity_Rs_425000_545000'].fillna( df['Power_Parity_Less_than_Rs_45000'] + df['Power_Parity_Rs_45000_90000'] + df['Power_Parity_Rs_90000_150000'] + 
    df['Power_Parity_Rs_150000_330000'] + df['Power_Parity_Rs_330000_425000']  + df['Power_Parity_Above_Rs_545000']) 
    df['Power_Parity_Above_Rs_545000']=df['Power_Parity_Above_Rs_545000'].fillna(df['Power_Parity_Less_than_Rs_45000'] + df['Power_Parity_Rs_45000_90000'] + df['Power_Parity_Rs_90000_150000'] + 
    df['Power_Parity_Rs_150000_330000'] + df['Power_Parity_Rs_330000_425000'] + df['Power_Parity_Rs_425000_545000'] ) 
# Fill 'Households_with_Telephone_Mobile_Phone_Both'
    df['Households_with_Telephone_Mobile_Phone_Both'] = df['Households_with_Telephone_Mobile_Phone_Both'].fillna(
    df['Households_with_Telephone_Mobile_Phone'] - df['Households_with_Telephone_Mobile_Phone_Landline_only'] - 
    df['Households_with_Telephone_Mobile_Phone_Mobile_only'])
    df['Households_with_Telephone_Mobile_Phone'] = df['Households_with_Telephone_Mobile_Phone'].fillna(
    df['Households_with_Telephone_Mobile_Phone_Landline_only'] + df['Households_with_Telephone_Mobile_Phone_Mobile_only'] + 
    df['Households_with_Telephone_Mobile_Phone_Both'])

# Fill 'Main_source_of_drinking_water_Tapwater_Households'
    df['Main_source_of_drinking_water_Tapwater_Households'] = df['Main_source_of_drinking_water_Tapwater_Households'].fillna(
    df['Main_drinking_water_Handpump_Tubewell_Borewell_Households'] + df['Main_drinking_water_Other_sources_Households'] + 
    df['Main_source_of_drinking_water_River_Canal_Households'] + df['Main_source_of_drinking_water_Spring_Households'] + 
    df['Main_source_of_drinking_water_Tank_Pond_Lake_Households'] + df['Main_source_of_drinking_water_Tubewell_Borehole_Households'] + 
    df['Main_source_of_drinking_water_Un_covered_well_Households'])

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
 #print(data.columns.tolist())

# Optional: Save missing data comparison to a CSV file for reporting
 comparison.to_excel('missing_data_comparison.xlsx', index=True)
 data_filled.to_excel('data_filled1.xlsx', index=True)

 #data=data.drop(columns=['Population','Literate','Workers','SC','ST','Total_Education','Power_Parity_Rs_150000_330000','Power_Parity_Rs_330000_545000','Power_Parity_Rs_45000_150000']) 
##################################################TASK 4 completed###########################################################################

####################################################TASK 5 BEGIN#############################################################################

# Step 1: Define the MongoDB connection URI
uri = "mongodb+srv://devisenthilkumar2024:tamil@cluster0.lzkkk4j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Step 2: Connect to the MongoDB cluster
client = MongoClient(uri)
collection = client.testdb.collectionpres

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
db_name = 'testpres'
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
create_table_query = "CREATE TABLE IF NOT EXISTS censusfinpres ("
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
data_df.to_sql('censusfinpres', con=engine, if_exists='replace', index=False)

def print_Sql():
# Step 11: Print a success message to confirm data insertion
  print("Data inserted successfully into MySQL")

# Print the data again for final verification
  print(data.columns.tolist()) 
  print(data_df.columns.tolist())

##################################################TASK 6 completed###########################################################################
tasknumber=8
while tasknumber!='0':
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
        print_new_state_name()
    elif tasknumber == '4':
        print_comparison()
    elif tasknumber == '5':
        print_Mongo()
    elif tasknumber == '6':
        print_Sql()
    
    