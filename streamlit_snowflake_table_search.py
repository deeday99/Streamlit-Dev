import streamlit as st
import snowflake.connector
import pandas as pd
from fuzzywuzzy import process

# Function to search tables in the Snowflake database
# 'LIKE ANY' is case-sensitive, so if you want case-insensitive matching use ILIKE ANY (snowflake supported)
def search_tables(query, cursor):
    # Execute SQL query to search tables
    cursor.execute(f"SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME ILIKE ANY'%{query}%'")
    results = cursor.fetchall()
    return results

# Perform fuzzy matching
    match = process.extractOne(query, table_names)
    if match and match[1] >= 70:  # Adjust threshold as needed
        return match[0]
    else:
        return None
    
# Function to fetch table data
def fetch_table_data(schema, table, cursor):
    cursor.execute(f"SELECT * FROM \"{schema}\".\"{table}\" LIMIT 10")  # Fetch first 10 rows
    data = cursor.fetchall()
    return data
# Function to search documents in the Snowflake database
#def search_documents(query, cursor):
    # Execute SQL query to search documents
    #cursor.execute(f"SELECT * FROM your_schema.documents WHERE document_text LIKE '%{query}%'")
  #  results = cursor.fetchall()
   # return results

# Streamlit app
def main():
    st.title("Snowflake Search")

    # Snowflake connection parameters
    conn = snowflake.connector.connect(
    user=' ',
    password=' ',
    account='', #this can be found going to your snowflake profile and selecting account -> 
                            #copy account URL should look like this https://ok81541.us-east-2.aws.snowflakecomputing.com
                            # use the characters before .aws.snowflakecomputing.com -> ok81541.us-east-2 for an example
    warehouse='',
    database='',
    role='' ,
    schema ='' ,
    )
    cursor = conn.cursor()

    # Search query input
    query = st.text_input("Enter search query:")

    # Perform search when query is provided
    if query:
        st.subheader("Table Search Results")
        table_results = search_tables(query, cursor)
        if table_results:
            selected_table = st.selectbox("Select a table:", [f"{result[0]}.{result[1]}" for result in table_results])
            if selected_table:
                schema, table = selected_table.split('.')
                st.subheader("Table Data")
                table_data = fetch_table_data(schema, table, cursor)
                df = pd.DataFrame(table_data, columns=[desc[0] for desc in cursor.description])
                st.write(df)  # Display table data as DataFrame
        else:
            st.write("No tables found matching the search query.")

       # st.subheader("Document Search Results")
       # document_results = search_documents(query, cursor)
       # if document_results:
         #   for document_result in document_results:
           #     st.write(document_result)  # Display document search results
       # else:
           # st.write("No documents found matching the search query.")

    # Close Snowflake connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
