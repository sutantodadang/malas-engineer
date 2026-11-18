def handler(cursor):
    return cursor.execute('SELECT * FROM orders')  # transport bypasses service
