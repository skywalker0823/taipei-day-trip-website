from crypt import methods
from unicodedata import category
from dotenv import load_dotenv
from flask import *
import pymysql
import os
load_dotenv()
connection=pymysql.connect(charset='utf8',db='website',host='127.0.0.1',password=os.getenv("DB_PASS"),port=3306,user='root')


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.secret_key=os.getenv("SECRET_KEY")


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
	ender=int(page)+11
	# keyword=request.args.get("keyword")
	with connection.cursor(pymysql.cursors.DictCursor) as cursor:
		got=cursor.execute("""SELECT id,name,category2,description,address,transport,mrt,latitude,longitude,images FROM sites WHERE id>=%s AND id<=%s""",(page,ender))
		result=cursor.fetchall()
		connection.commit()
		if got != 0:
			summary=[]
			for site in result:
				sets={"nextPage":int(page)+1,"data":[{"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}]}
				summary.append(sets)
			return jsonify(summary)
		return jsonify({"error":True,"message":"查無資料"})

@app.route("/api/attraction/<attractionId>", methods=["GET"])
def api_atid(attractionId):
	with connection.cursor(pymysql.cursors.DictCursor) as cursor:
		got=cursor.execute("""SELECT id,name,category2,description,address,transport,mrt,latitude,longitude,images FROM sites WHERE id=%s""",(attractionId))
		site=cursor.fetchone()
		connection.commit()
		if got!=0:
			summary={"data":{"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}}
			return jsonify(summary)
		return jsonify({"error":True,"message":"查無資料"})


if __name__=="__main__":
	app.run(debug=True, port=3000)