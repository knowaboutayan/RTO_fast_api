
import mysql.connector
import mysql.connector.errors as snow_err
import dotenv
import os



def connection():
    dotenv.load_dotenv()
    try:
        conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"), 
        database=os.getenv("DB_NAME"), 
        user=os.getenv("DB_USERNAME"), 
        password=os.getenv("DB_PASSWORD"), 
        port=os.getenv("DB_PORT")
        )
    except snow_err.DatabaseError as err:
        print(f'!!!ERR!!! DATABASE NOT FOUND {err}')
        return 1
    except Exception as err:
        print(f'!!!ERR!!! SNOWFLAKE CONNECTION FAILD {err}')
        return 1
    else:
        print("::SNOWFLAKE CONNECTED SUCCCESSFULLY::")
        return conn



def query_runner(*,sql_query):
    db_conn = connection()
    if db_conn == 1:
        print('!!!ERR!!! not found db connection')
        return 1
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
    except Exception as err:
        print(f'!!!ERR!!! QUERY EXECUTION FAILED {err}')
        return 1
    else:
        print('::QUERY EXECUTION SUCCESSFUL::')
        print(data)
        cursor.close()
        db_conn.close()
        return data


# query_runner(sql_query='SELECT * FROM vehicle_details')








