from models import db, Document, CityRecord
import MySQLdb
from datetime import date
import os
import subprocess

DB = MySQLdb.connect(host="10.155.146.60", user="root", passwd="gpp369063", db="publications")
C = DB.cursor()
	
	
def index_document():

	C.execute("SELECT * FROM document")
	records = C.fetchall()
	
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
	
	
def index_city_record(year):
		
		path = '/data/cityRecordTxts/' + year + '/'
				
		for folder in os.listdir(path):
			filepath = path + folder
			
			for filename in os.listdir(filepath):
				file_split = filename.strip('.txt').split('_')
				file_date = date(int(file_split[-3]), int(file_split[-2]), int(file_split[-1]))
				
				rec_title = (' - ').join(file_split[:-3]).replace('CityRecord','City Record').replace('ComptrollerReport', 'Comptroller Report').replace('StatedMeeting','City Council Stated Meeting') + ' - ' + file_date.strftime("%B %d, %Y")
				
				infile = open(filepath + '/' + filename, 'r')
				lines = infile.readlines()
				doc = ''
				for line in lines:
					doc += ''.join([i if ord(i) < 128 else ' ' for i in line])
					
				rec_description = 'The City Record is the official journal of the City of New York. It is published each weekday except legal holidays and contains official legal notices produced by New York City agencies. Announcements published in The City Record include:\nupcoming public hearings and meetings; procurement bid solicitations; selected court decisions; bid awards; public auctions and other property disposition actions; official rules proposed and adopted by City agencies.\nProcurement bid solicitation notices afford vendors the opportunity to compete for New York City\'s $17 billion worth of contracts for various categories of goods and services for over 100 agencies and other governmental organizations.'
			
				db.session.add(CityRecord(title=rec_title,
										description=rec_description,
										date_created=file_date,
										filename=filename,
										num_access=0,
										agency='Citywide Admin Svcs',
										category='Government Policy',
										type='Serial Publication',
										url='/data/cityRecordPdfs/' + year + '/' + filename.replace('txt','pdf'),
										pub_or_foil='Publication',
										docText=doc))							
			db.session.commit()


def add_sample_entries():

	infile = open('/export/local/admin/government-publications-portal/CityRecord_Apr_01_2008.txt', 'r')
	lines = infile.readlines()
	doc = ''
	for line in lines:
		doc += ''.join([i if ord(i) < 128 else ' ' for i in line])
# 	print doc
	db.session.add(CityRecord(id=100000,
							title='CityRecord_Apr_01_2008',
							description = 'CityRecord_Apr_01_2008',
							date_created=datetime.date(7,1,1),
							filename = 'CityRecord_Apr_01_2008',
							num_access=0,
							agency='Aging',
							category='Education',
							type='Annual Report',
							url='',
							pub_or_foil='Publication',
							docText = doc))
	db.session.commit()