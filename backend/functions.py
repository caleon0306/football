import psycopg2 as psy


connection = psy.connect(database="fantasy_football", user="postgres",password="4Wihicis!")
cursor = connection.cursor()

connection.commit()