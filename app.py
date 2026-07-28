import csv
import psycopg2

try:
    # 1. Open the secure connection to your local PostgreSQL server
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Fridaous@123"  # Kept your database password from the image
    )
    cursor = connection.cursor()

    # 2. Read the external data document
    print("Opening file data source...")
    with open('students_data.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        # 3. Loop through every single row inside the spreadsheet automatically
        for row in csv_reader:
            # Clean up the trailing empty spaces using .strip()
            clean_name = row['fullname'].strip()
            course = row['course_name'].strip()
            
            print(f"Processing: {clean_name} -> {course}")
            
            # 4. Fetch the matching parent Course ID dynamically from your catalog
            cursor.execute("SELECT course_id FROM courses WHERE course_name = %s;", (course,))
            course_result = cursor.fetchone()
            
            if course_result:
                course_id = course_result[0]
                
                # 5. Load the clean record straight into your student database table layout
                cursor.execute("""
                    INSERT INTO kwasu_students (fullname, assigned_course_id) 
                    VALUES (%s, %s);
                """, (clean_name, course_id))
            else:
                print(f"Skipping {clean_name}: Course '{course}' does not exist in master catalog.")

    # 6. Save all the bulk injections permanently to your server layout
    connection.commit()
    print("\nBulk file automation completed successfully!")

    cursor.close()
    connection.close()

except Exception as error:
    print(f"Pipeline Automation Failed: {error}")