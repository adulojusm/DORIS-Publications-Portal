from models import db, Document
import MySQLdb

def index_database():
	mysqldb = MySQLdb.connect(host="10.155.146.60", user="root", passwd="gpp369063", db="publications")
	c = mysqldb.cursor()
	c.execute("SELECT * FROM document")
	records = c.fetchall()
	
	for record in records:
		db.session.add(Document(id=record[0],
								title=record[1],
								description=record[2],
								date_created=record[3],
								filename=record[4],
								num_access=record[7],
								agency=record[8],
								category=record[9],
								type=record[10],
								url=record[11],
								pub_or_foil=record[12]))
	db.session.commit()