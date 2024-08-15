
import snowflake.connector
import snowflake.connector.errors as snow_err
import dotenv
import os



def connection():
    dotenv.load_dotenv()
    try:
        conn = snowflake.connector.connect(
            user='teamthreecoders',
            password='Teamthreecoders@333',
            account='xmuamex-vx46985',
            warehouse='TRAFFIC_FINE_WAREHOUSE',
            database='TRAFFIC_FINE_DB',
            schema='TRAFFIC_FINE_SCHEMA'
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








