import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('ecg_data.db')
cursor = conn.cursor()

# Execute a query to fetch the first 5 rows from the ECG table
cursor.execute('SELECT * FROM ECG LIMIT 5')
rows = cursor.fetchall()

# Print the fetched rows
print("First 5 rows from ECG table:")
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
