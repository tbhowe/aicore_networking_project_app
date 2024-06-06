import psycopg2
import boto3
import json
from botocore.exceptions import ClientError

def load_credentials(secret_name, region_name):
    """Retrieve database credentials from AWS Secrets Manager."""
    session = boto3.session.Session(region_name=region_name)
    client = session.client(service_name='secretsmanager')
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Unable to retrieve secret: {e}")
        return None
    else:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)

# Use the secret named 'db_credentials' in the 'eu-north-1' region
creds = load_credentials('db_credentials', 'eu-north-1')

if creds:
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
else:
    print("Failed to load credentials. Cannot proceed.")
