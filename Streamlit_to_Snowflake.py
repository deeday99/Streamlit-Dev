# WRITE THE HEADER
st.header("Student At-Risk Table")

# ADD THE SIDEBAR AND SELECT BOX
with st.sidebar:
    # OPTIONS FOR THE SELECT BOX
    options = ["All"]  # Initial option to display all data
    grade_level_options = ["All"] 
    
    # SET THE SQL COMMAND TO LOAD THE DATAFRAME
    selectbox_sql = """
        SELECT AtRiskType
        FROM STUDENTS.PUBLIC.AT_RISK_STUDENTS
        GROUP BY AtRiskType;
        """
    # COLLECT THE DATA VALUES INTO A DF
    selectbox_df = session.sql(selectbox_sql).collect()
    for row in selectbox_df:
        options.append(row[0])  # Add each At-Risk type to options list

    # SET THE SQL COMMAND TO LOAD THE GRADE LEVELS
    selectbox_sql = """
        SELECT DISTINCT GradeLevel
        FROM STUDENTS.PUBLIC.AT_RISK_STUDENTS
        ORDER BY GradeLevel;
        """
    # COLLECT THE DATA VALUES INTO A DF
    selectbox_df = session.sql(selectbox_sql).collect()
    for row in selectbox_df:
        grade_level_options.append(row[0])  # Add each Grade Level to options list
    
    # CREATE THE SELECT BOXES; STORE SELECTED VALUES
    var_atrisk_type = st.selectbox(label="Select AT-RISK Type:", options=options)
    var_grade_level = st.selectbox(label="Select Grade Level:", options=grade_level_options)
    sort_order = st.selectbox(label="Sort Order:", options=["Ascending", "Descending"])

# BUILD SQL COMMAND TO READ THE TABLE
sql = """
SELECT
    AtRiskType AS AT_RISK_TYPE,
    StudentName AS Student_Name,
    GradeLevel AS Grade_Level,
    ID AS ID
FROM
    STUDENTS.PUBLIC.AT_RISK_STUDENTS
"""
# ADD WHERE CLAUSES BASED ON SELECTED VALUES IN THE SELECTBOX
if var_atrisk_type != "All":
    sql += f" WHERE AtRiskType = '{var_atrisk_type}'"
if var_grade_level != "All":
    if "WHERE" in sql:
        sql += f" AND GradeLevel = {var_grade_level}"
    else:
        sql += f" WHERE GradeLevel = {var_grade_level}"

# ADD ORDER BY CLAUSE BASED ON SELECTED SORT ORDER
if sort_order == "Ascending":
    sql += " ORDER BY Grade_Level ASC"
else:
    sql += " ORDER BY Grade_Level DESC"

# QUERY SNOWFLAKE
df = session.sql(sql).collect()

# WRITE TO SCREEN
st.dataframe(data=df, use_container_width=True)