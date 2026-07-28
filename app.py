import psycopg2

try:
    # 1. Establish secure server link
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Fridaous@123"
    )
    cursor = connection.cursor()

    # 2. Run the Aggregated Metrics Report
    reporting_query = """
    SELECT 
        courses.course_name,
        COUNT(kwasu_students.student_id) AS total_enrolled_students
    FROM kwasu_students
    INNER JOIN courses 
        ON kwasu_students.assigned_course_id = courses.course_id
    GROUP BY courses.course_name
    HAVING COUNT(kwasu_students.student_id) > 2;
    """
    
    print("Running Live Enrollment Metrics Report...")
    cursor.execute(reporting_query)
    report_rows = cursor.fetchall()

    # 3. Print out clean Executive Business Intelligence Analytics
    print("\n=======================================================")
    print("       KWASU EXECUTIVE BUSINESS METRICS LOG            ")
    print("=======================================================")
    for record in report_rows:
        course_name = record[0]
        enrollment_count = record[1]
        
        print(f"📊 TRACK:  {course_name.upper()}")
        print(f"👥 METRIC: {enrollment_count} Active Enrolled Students")
        print("-------------------------------------------------------")
    print("Report compiled successfully by pipeline core.\n")

    cursor.close()
    connection.close()

except psycopg2.OperationalError as db_error:
    print(f"\n❌ PIPELINE DATABASE CONNECTION FAILURE: {db_error}")
except Exception as general_error:
    print(f"\n❌ METRIC EXTRACTION CRASHED: {general_error}")