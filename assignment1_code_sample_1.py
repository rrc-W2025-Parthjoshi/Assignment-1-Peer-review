import os
import pymysql
from urllib.request import urlopen

db_config = {
    'host': 'mydatabase.com',
    'user': 'admin',
    'password': 'secret123' # Database credentials are hard-coded in the source code. This is a security risk if the code is shared or pushed to GitHub. Credentials should be loaded from environment variables or a secure config.
}

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input

def send_email(to, subject, body):
    os.system(f'echo {body} | mail -s "{subject}" {to}') # os.system() is used with user-controlled input. This can lead to command injection if the input contains shell characters. subprocess or a proper email library should be used instead.

def get_data():
    url = 'http://insecure-api.com/get-data' # External API call uses HTTP instead of HTTPS. Data can be intercepted or modified in transit. HTTPS should be used to ensure secure communication.
    data = urlopen(url).read().decode()
    return data

def save_to_db(data):
    query = f"INSERT INTO mytable (column1, column2) VALUES ('{data}', 'Another Value')" # SQL query is built using string formatting (f-string). This makes the code vulnerable to SQL injection if data contains. special characters or malicious input. Parameterized queries should be used.
    connection = pymysql.connect(**db_config) # Database connection and cursor are not safely managed. If an exception occurs, the connection may not be closed properly. Using context managers (with) or try/finally is recommended.
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
