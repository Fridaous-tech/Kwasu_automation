import csv
import psycopg2
import os

try:
    # 1. DEFENSIVE CHECK: Verify if the source file actually exists before running
    file_path = 'students_data.csv'
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The input document '{file_path}' was not found in this folder.")

    # 2. Establish connection to your database server
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Fridaous@123"  # Testing incorrect password
    )
    cursor = connection.cursor()

    print("Opening file data source safely...")
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            clean_name = row['fullname'].strip()
            course = row['course_name'].strip()
            
            cursor.execute("SELECT course_id FROM courses WHERE course_name = %s;", (course,))
            course_result = cursor.fetchone()
            
            if course_result:
                course_id = course_result
                cursor.execute("""
                    INSERT INTO kwasu_students (fullname, assigned_course_id) 
                    VALUES (%s, %s);
                """, (clean_name, course_id))
            else:
                print(f"⚠️ Warning: Skipping '{clean_name}'. Course '{course}' does not exist.")

    connection.commit()
    print("🚀 Ingestion workflow finished successfully!")

# =====================================================================
# UPDATED COMPATIBLE FAULT-TOLERANCE BLOCKS
# =====================================================================
except FileNotFoundError as file_error:
    print(f"\n❌ FILE TRACKING ERROR: {file_error}")
    print("💡 Fix: Make sure 'students_data.csv' is saved in this exact folder.")

except psycopg2.OperationalError as db_error:
    # This block now beautifully catches both wrong passwords and server connection drops!
    error_msg = str(db_error)
    print("\n❌ DATABASE CONNECTION OR ACCESS ERROR")
    if "password authentication failed" in error_msg:
        print("🔒 Security Access Denied: Your database password is incorrect.")
    else:
        print(f"📡 Connection Failure: Cannot reach your database server. Details: {db_error}")
    print("💡 Fix: Check your database password or make sure pgAdmin 4 is running.")

except Exception as unexpected_error:
    print(f"\n❌ UNEXPECTED CRASH CAUGHT: {unexpected_error}")

# =====================================================================
# THE CLEANUP BLOCK
# =====================================================================
finally:
    if 'connection' in locals() and connection is not None:
        cursor.close()
        connection.close()
        print("🔒 Database server connection closed cleanly by fallback handler.")