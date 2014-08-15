#Parse.py

#Used to parse JSON files to Postgres Database

import psycopg2
import json
import os
from constants import DBNAME, USERNAME, HOST, PASSWORD 


connect = "dbname= %s user= %s host= %s password= %s " % (DBNAME,USERNAME, HOST, PASSWORD)
conn = psycopg2.connect(connect)

cur = conn.cursor()

#Change to directory of JSON files
rootdir = '../kevinbacon/films'

count =10

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
     
		fileData= json.load(open("../kevinbacon/films/"+file))

		movieTitle= fileData['film']['name'].replace("'", "")

		sql="INSERT INTO movies (id, title) VALUES ("+ str(count) + ",'" + movieTitle + "')"
		cur.execute(sql)

		conn.commit()

		for actor in fileData['cast']:
			name = actor['name'].replace("'", "")
			cur.execute("INSERT INTO acted (movie_id, actor_name) VALUES ("+ str(count)+ ",'" + name + "')")

		conn.commit()
		count+=1











