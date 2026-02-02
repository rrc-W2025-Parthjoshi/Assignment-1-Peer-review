import os
import subprocess
import pymysql
from urllib.request import urlopen

# Read DB config from environment 
db_config = {
    'host': os.environ.get('DB_HOST', 'mydatabase.com'),
    'user': os.environ.get('DB_USER', 'app_user'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'mydb'),
    'port': int(os.environ.get('DB_PORT', '3306'))
}

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input

def send_email(to, subject, body):
    # Avoid shell injection by not using os.system()
    subprocess.run(["mail", "-s", subject, to], input=body, text=True)

def get_data():
    # Use HTTPS to protect data in transit
    url = 'https://insecure-api.com/get-data'
    data = urlopen(url).read().decode()
    return data

def save_to_db(data):
    # Use parameterized query to prevent SQL injection
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query, (data, 'Another Value'))
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
