import psycopg2
def get_connection():
    connection = psycopg2.connect(host='127.0.0.1', database='controle_codigo',
                                  user='postgres', password='postgres',
                                  port=5432)
    return connection