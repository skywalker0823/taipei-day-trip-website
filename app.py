from crypt import methods
from unicodedata import category
# from dotenv import load_dotenv
from flask import *
import pymysql
import os
import ast
# load_dotenv()
connection=pymysql.connect(charset='utf8',db='website',host='127.0.0.1',password="",port=3306,user='root')


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False
# app.secret_key=os.getenv("SECRET_KEY")


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


@app.route("/api/attractions", methods=["GET"])
def api_attr():
	page=request.args.get("page")
	keyword=request.args.get("keyword")
	if keyword!=None:
		ender=(int(page)+1)*12
		page=ender-12
		print("here",page,ender)
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			got=cursor.execute("""SELECT id,name,category2,description,address,transport,mrt,latitude,longitude,images FROM sites WHERE name like %s LIMIT %s,%s """,(("%"+keyword+"%"),page,ender))
			result=cursor.fetchall()
			count=cursor.rowcount
			connection.commit()
			if got != 0:
				summary=[]
				if count<12:
					for site in result:
						a_set={"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}
						a_set["images"]=ast.literal_eval(a_set["images"])
						summary.append(a_set)
					# summary[0]["data"][0]["images"]=ast.literal_eval(summary[0]["data"][0]["images"])
					final={"nextPage":None,"data":summary}
					return jsonify(final)
				for site in result:
					a_set={"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}
					a_set["images"]=ast.literal_eval(a_set["images"])
					summary.append(a_set)
				# summary[0]["data"][0]["images"]=ast.literal_eval(summary[0]["data"][0]["images"])
				final={"nextPage":int(ender)//12+1,"data":summary}
				return jsonify(final)
			return jsonify({"error":True,"message":"查無資料"})
	else:
		if page==None:
			page=0
		ender=(int(page)+1)*12
		page=ender-11
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			got=cursor.execute("""SELECT id,name,category2,description,address,transport,mrt,latitude,longitude,images FROM sites WHERE id>=%s AND id<=%s """,(page,ender))
			result=cursor.fetchall()
			count=cursor.rowcount
			connection.commit()
			if got != 0:
				summary=[]
				if count<12:
					for site in result:
						a_set={"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}
						a_set["images"]=ast.literal_eval(a_set["images"])
						summary.append(a_set)
						print(summary)
					# summary[0]["data"][0]["images"]=ast.literal_eval(summary[0]["data"][0]["images"])
					final={"nextPage":None,"data":summary}
					return jsonify(final)
				for site in result:
					a_set={"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}
					a_set["images"]=ast.literal_eval(a_set["images"])
					summary.append(a_set)
					# summary[0]["data"][0]["images"]=ast.literal_eval(summary[0]["data"][0]["images"])

				final={"nextPage":int(ender)//12,"data":summary}
				return jsonify(final)
			return jsonify({"error":True,"message":"查無資料"})
		
		

@app.route("/api/attraction/<attractionId>", methods=["GET"])
def api_atid(attractionId):
	with connection.cursor(pymysql.cursors.DictCursor) as cursor:
		got=cursor.execute("""SELECT id,name,category2,description,address,transport,mrt,latitude,longitude,images FROM sites WHERE id=%s""",(attractionId))
		site=cursor.fetchone()
		connection.commit()
		if got!=0:
			summary={"data":{"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}}
			# summary[0]["data"][0]["images"]=ast.literal_eval(summary[0]["data"][0]["images"])
			summary["data"]["images"]=ast.literal_eval(summary["data"]["images"])
			return jsonify(summary)
		return jsonify({"error":True,"message":"查無資料"})


if __name__=="__main__":
	app.run(host='0.0.0.0',port=3000)