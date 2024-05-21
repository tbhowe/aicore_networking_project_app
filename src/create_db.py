import psycopg2
import yaml

# Load credentials from the YAML file
with open('creds.yaml', 'r') as file:
    creds = yaml.safe_load(file)

# Establish connection to the PostgreSQL server
conn = psycopg2.connect(
    dbname='postgres',  # Connect to the default database to perform admin tasks
    user=creds['username'],
    password=creds['password'],
    host=creds['host'],
    port=creds['port']
)
conn.autocommit = True  # Enable autocommit for database creation

# Create a cursor object using the connection
cursor = conn.cursor()

# Specify the name of the database you want to create
db_name = creds['database_name']

# Check if the database already exists
cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s", (db_name,))
db_exists = cursor.fetchone()

# Create the database if it does not exist
if not db_exists:
    cursor.execute(f"CREATE DATABASE {db_name}")
    print(f"Database '{db_name}' created successfully.")
else:
    print(f"Database '{db_name}' already exists.")

# Close the cursor and connection
cursor.close()
conn.close()
