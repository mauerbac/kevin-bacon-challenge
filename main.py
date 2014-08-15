#Main.py

import sys
import psycopg2
from constants import DBNAME, USERNAME, HOST, PASSWORD 


#connect to DB
connect = "dbname= %s user= %s host= %s password= %s " % (DBNAME,USERNAME, HOST, PASSWORD)
conn = psycopg2.connect(connect)
cur = conn.cursor()


def main():
	#ask user for target actor
	#target= raw_input("What is the actor ").replace("'", "")
	#get input from command line
	try:
		sys.argv[1]
	except:
		print "No Actor provided"
		sys.exit()

	target= ' '.join(sys.argv[1:])

	#list of actors explored
	global actorsExplored, nextActors, flag, level

	#list of actors explored
	actorsExplored=[]

	#temp list of actors we need to store
	nextActors=[]
 
	#query degree 1 actors (all actors kevin bacon worked with directly)
	rows = getActors("Kevin Bacon")
	actorsExplored.append("Kevin Bacon")

	#set found flag to false 
	flag=False

	level=1

	result=[]

	#check if target is in degree 1
	for actor in rows:
		if(actor[0] == target):
			flag=True
			result.append((actor[0],actor[1]))
			break

    #recursively dive deeper 
	if(not(flag)):
		(targetActor, targetMovie, prevActor, prevMovie, level) = checkDegree(target,rows,level)
		if(level==2):
			result.append((targetActor,targetMovie))
			result.append((prevActor,prevMovie))

		else:
			level-=1
			result.append((targetActor,targetMovie))
			checkDegree(prevActor,rows,level)


	result.append(("Kevin Bacon"," "))

	printList(result)
	print "Degree ",level


def getActors(actor):
	global cur

	sql= "SELECT DISTINCT acted.actor_name, movies.title FROM acted, movies WHERE movies.id=acted.movie_id AND movies.id IN (SELECT movies.id FROM acted,movies WHERE movies.id=acted.movie_id AND acted.actor_name= '%s' );" % (actor)
	try:
		cur.execute(sql)
	except Exception, e:
		print "There was an SQL error"
	return cur.fetchall()


def checkDegree(target,rows,level):
	global actorsExplored, nextActors,flag

	while(not(flag)):
			level+=1

			for actor in rows:
				if actor[0] not in actorsExplored:
					nextActors.append((actor[0],actor[1]))
					actorsExplored.append(actor[0])
					temp=getActors(actor[0])
					#check if this actors peers is target
					for actor1 in temp:
						if(actor1[0] == target):
							flag=True
							return actor1[0], actor1[1], actor[0], actor[1], level
			rows= nextActors
			if(len(nextActors)==0):
				break
			nextActors=[]
			level+=1 
	print "No connections/paths found with given database"
	sys.exit(0)
	return 0


def printList(data):
	for entry in data[:-1]:
		print entry[0] + " (" + entry[1] + ") -> ",

	print "Kevin Bacon"


if __name__ == "__main__":
	main()