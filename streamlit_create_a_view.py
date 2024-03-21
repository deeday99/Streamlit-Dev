import streamlit as st
import snowflake.connector

# Function to create a view in the Snowflake database
def create_view(cursor, schema_name, view_name, table_name, condition=None):
    # Construct the CREATE VIEW query
    create_view_query = f"CREATE OR REPLACE VIEW {schema_name}.{view_name} AS SELECT * FROM {table_name}"
    if condition:
        create_view_query += f" WHERE {condition}"
    
    print("Debug: CREATE VIEW query:", create_view_query)  # Debug print
    
    try:
        # Execute the CREATE VIEW query
        cursor.execute(create_view_query)
        # Display success message if view creation is successful
        st.success(f"View '{view_name}' created successfully in schema '{schema_name}'!")
    except Exception as e:
        # Display error message if an exception occurs during view creation
        st.error(f"Error creating view '{view_name}': {e}")


# Streamlit app
def main():
    st.title("Create View in Snowflake")

    # Snowflake connection parameters
    conn = snowflake.connector.connect(
        user='your_username',
        password='your_password',
        account='your_account',
        warehouse='your_warehouse',
        database='your_database',
        role='your_role'
    )
    cursor = conn.cursor()

   # User input for schema name (what schema you want to put the view in)
    schema_name = st.text_input("Enter schema name:")
    
    # User input for view name (what do you want to name your view)
    view_name = st.text_input("Enter view name:")
    
    # User input for table name (what table are you using to create the view)
    table_name = st.text_input("Enter table name:")
    
    # User input for condition (optional)
    condition = st.text_input("Enter condition (optional):")
    
    # Button to create the view
    if st.button("Create View"):
        create_view(cursor, schema_name, view_name, table_name, condition)

    # Close Snowflake connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()