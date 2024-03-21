import streamlit as st
import snowflake.connector
import pandas as pd
from fuzzywuzzy import process

# Function to search views in the Snowflake database
def search_views(query, cursor):
    cursor.execute(f"SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_NAME ILIKE ANY'%{query}%'")
    results = cursor.fetchall()
    return results

# Function to perform fuzzy matching
def fuzzy_match(query, table_names):
    match = process.extractOne(query, table_names)
    if match and match[1] >= 70:  # Adjust threshold as needed
        return match[0]
    else:
        return None
    
# Function to fetch view data
def fetch_view_data(schema, view, cursor):
    cursor.execute(f"SELECT * FROM \"{schema}\".\"{view}\" LIMIT 10")
    data = cursor.fetchall()
    return data

# Streamlit app
def main():
    st.title("Snowflake Search")

    # Snowflake connection parameters
    conn = snowflake.connector.connect(
        user='your_username',
        password='your_password',
        account='your_account',
        warehouse='your_warehouse',
        database='your_database',
        role='your_role',
        schema='your_schema',
    )
    cursor = conn.cursor()

    # Search query input
    query = st.text_input("Enter search query:")

    # Perform search when query is provided
    if query:
        st.subheader("View Search Results")
        view_results = search_views(query, cursor)
        if view_results:
            selected_view = st.selectbox("Select a view:", [f"{result[0]}.{result[1]}" for result in view_results])
            if selected_view:
                schema, view = selected_view.split('.')
                st.subheader("View Data")
                view_data = fetch_view_data(schema, view, cursor)
                df = pd.DataFrame(view_data, columns=[desc[0] for desc in cursor.description])
                st.write(df)  # Display view data as DataFrame
        else:
            st.write("No views found matching the search query.")

    # Close Snowflake connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
