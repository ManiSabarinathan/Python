import urllib.parse
import requests
import mysql.connector
import json
import time

#create table apple_reviews (authorURIData varchar(10) DEFAULT NULL, authorNameData varchar(10) DEFAULT NULL, im_versionData varchar(10) DEFAULT NULL, im_ratingData varchar(10) DEFAULT NULL, titleData varchar(10) DEFAULT NULL,contentData varchar(100) DEFAULT NULL )

def main(mydb,myCursor):
	sql = "INSERT INTO apple_reviews (authorURIData, authorNameData,im_versionData,im_ratingData,titleData,contentData) VALUES (%s, %s)"
	
	main_api = "https://itunes.apple.com/us/rss/customerreviews/id=341036067/json"
	try:
		response_data = requests.get(main_api).json()
		print("Inside Response Block")
		#print(response_data)
		#print(type(response_data))
		
		print("Parsing data..")
		parse_Data(response_data,mycursor)
		
		
		#print("Updating DB...");
		#update_DB(mydb,myCursor,sql);
		#print("After update()...");
		
	except Exception as ce:
		print("Exception block ");
		print(ce);
	
def parse_Data(response, mycursor):
		print(response)
		obj = json.dumps(response)	
		loaded_r = json.loads(obj)
		entryData=loaded_r["feed"]["entry"]
		list_Length=len(entryData)
	
		for i in range(0, list_Length):
			print("Sleeping for 10 milli seconds before iterating ")
			#time.sleep(0.300)
			authorURIData=entryData[i]["author"]["uri"]["label"]
			authorNameData=entryData[i]["author"]["name"]["label"]
			im_versionData=entryData[i]["im:version"]["label"]
			im_ratingData=entryData[i]["im:rating"]["label"]
			titleData=entryData[i]["title"]["label"]
			contentData=entryData[i]["content"]["label"]
			val=(authorURIData,authorNameData,im_versionData,im_ratingData,titleData,contentData)
			#print(entryData)
			#print(authorURIData)
			#print(authorNameData)
			#print(im_versionData)
			#print(im_ratingData)
			#print(titleData)
			#print(contentData)
		update_DB_Test(mycursor,val)	

	
#def update_DB(mydb,mycursor,sql):
#	val = ("John", "Highway 21");
#	mycursor.execute(sql, val);
#	mydb.commit()
	
def update_DB_Test(mycursor,val):
	print("Value is ==> ",val)
	val = ("John", "Highway 21");
	mycursor.execute(sql, val);
	#mydb.commit()



if __name__ == '__main__':
	mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="customers")
	myCursor = mydb.cursor();
	main(mydb,myCursor)