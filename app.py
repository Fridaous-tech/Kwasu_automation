import psycopg2

try:
    # 1. Establish connection to local database
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Fridaous@123"
    )
    cursor = connection.cursor()

    # 2. Execute the multi-table Relational JOIN query
    query = """
    SELECT 
        kwasu_students.student_id,
        kwasu_students.fullname,
        courses.course_name,
        courses.faculty
    FROM kwasu_students
    INNER JOIN courses 
    ON kwasu_students.assigned_course_id = courses.course_id;
    """
    cursor.execute(query)
    records = cursor.fetchall()
    
    # 3. Print out clean structured business intelligence logs
    print("\n=======================================================")
    print("      KWASU RELATIONAL DATA PIPELINE ACTIVE            ")
    print("=======================================================")
    for row in records:
        print(f"Student ID: {row[0]}")
        print(f"Name:       {row[1]}")
        # Capitalize the track name to show data formatting control
        print(f"Track:      {row[2].upper()}") 
        print(f"Faculty:    {row[3]}")
        print("-------------------------------------------------------")

    cursor.close()
    connection.close()

except Exception as error:
    print(f"Pipeline Execution Failed: {error}")