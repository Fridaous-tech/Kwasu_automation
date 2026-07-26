import psycopg2

try:
    # 1. Establish database connection
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Fridaous@123"  # Verified password from your screenshot
    )
    cursor = connection.cursor()

    # 2. Write Data (Data Ingestion Phase)
    print("Ingesting new record into database...")
    cursor.execute("""
        INSERT INTO kwasu_students (fullname, skill_track) 
        VALUES ('Global Consultant', 'AI Agent Engineering');
    """)
    connection.commit() # Save changes permanently

    # 3. Read Data (Data Retrieval Phase)
    cursor.execute("SELECT * FROM kwasu_students;")
    records = cursor.fetchall() # Reads the rows after they are updated
    
    # 4. Display Data clean and un-cluttered
    print("\n--- RETRIEVING PIPELINE RECORDS ---")
    for row in records:
        print(f"ID: {row[0]} | Student: {row[1]} | Track: {row[2]}")
    print("------------------------------------\n")

    cursor.close()
    connection.close()

except Exception as error:
    print(f"Pipeline Error: {error}")