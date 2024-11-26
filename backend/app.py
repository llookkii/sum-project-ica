import os
import psycopg2
from flask import Flask, request, jsonify
from psycopg2 import sql

app = Flask(__name__)

# Database connection parameters from environment variables or secrets
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'sumdb')
DB_USER = os.getenv('DB_USER', 'dbuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

# Function to create the database table if it doesn't exist


def create_table():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS sums (
            id SERIAL PRIMARY KEY,
            num1 FLOAT NOT NULL,
            num2 FLOAT NOT NULL,
            sum_result FLOAT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating table: {e}")


@app.route('/calculate', methods=['POST'])
def calculate_sum():
    data = request.get_json()
    num1 = data.get('num1')
    num2 = data.get('num2')
    sum_result = num1 + num2

    # Insert the numbers and result into the database
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        insert_query = '''
        INSERT INTO sums (num1, num2, sum_result)
        VALUES (%s, %s, %s);
        '''
        cursor.execute(insert_query, (num1, num2, sum_result))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'sum': sum_result}), 200

    except Exception as e:
        print(f"Error inserting into database: {e}")
        return jsonify({'error': 'Database error'}), 500


if __name__ == '__main__':
    # Create table on app startup
    create_table()
    app.run(host='0.0.0.0', port=5000)
