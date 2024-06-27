import psycopg2 as psy

#function to run a query to commit to fantasy_football database
def run_commit_query(query = ""):
    if query == "":
        return
    connection = psy.connect(database="fantasy_football", user="postgres",password="4Wihicis!")
    #connect cursor to database
    cursor = connection.cursor()
    #run query
    cursor.execute(query)
    #commit changes
    connection.commit()
    #close cursor and connection
    cursor.close()
    connection.close()

#function to run a query and return a row from query
def fetch_one(query = ""):
    if query == "":
        return
    connection = psy.connect(database="fantasy_football", user="postgres",password="4Wihicis!")
    cursor = connection.cursor()
    cursor.execute(query)
    #fetch a single row
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

#fetch all rows for a query
def fetch_all(query = ""):
    if query == "":
        return
    connection = psy.connect(database="fantasy_football", user="postgres",password="4Wihicis!")
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result