
# Census Data Cleaning and Transfer

This Python script reads census data from an Excel file, cleans and transforms it, and then inserts it into MongoDB and transfers it to a MySQL database and finally visualizing in streamlit.

**Features**

- Reads Excel data using pandas
- Renames columns for clarity
- Standardizes state names
- Updates state information based on a Word document
- Handles missing values (customizable logic)
- Inserts data into MongoDB
- Transfers data from MongoDB to MySQL

**Requirements**

- Python 3.x
- pandas
- re
- numpy
- pymongo
- mysql.connector (or mysql)
- sqlalchemy
- docx

**Usage**

1. Update file paths, database credentials, and table name in the script.
2. Install required libraries.
3. Run `python main.py`.

**. Streamlit App Structure:
Title: The app displays a title, "Census Data Analysis Dashboard."
State Selection Dropdown: A dropdown menu allows users to select a state from a list of unique values in the StateUT column of the DataFrame. "All States" is included as an option for displaying aggregated data.
Conditional Data Filtering: Based on the selected state, the DataFrame is either left unchanged or filtered to include only records for that state.

**. Query Selection Dropdown:
Query Options: A dropdown provides choices for various queries users can visualize (modify these options based on your data).
Query Processing: Depending on the selected query, the code performs specific data aggregations and transformations using Pandas.
Visualization Generation: Streamlit's st.plotly_chart function displays the results as interactive charts created with Plotly Express.


