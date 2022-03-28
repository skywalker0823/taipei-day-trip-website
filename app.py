from crypt import methods
from unicodedata import category
# from dotenv import load_dotenv
from flask import *
import pymysql
import os
import ast
from flask import render_template as rt
from pymysql import NULL
from modules.looper import looper
from member_manage import member_manage
from booking_manage import booking_manage
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from dbutils.pooled_db import PooledDB



# POOL = PooledDB(
#     creator=pymysql,  # Which DB module to use
#     maxconnections=6,  # Allowed max connection, 0 and None means no limitations.
#     mincached=2,  # Least connection when created, 0 means don't.
#     blocking=True,  # Queue when there is no connection avaliable. True = wait；False = No waits, and report error.
#     ping=0, # Check if Mysql service is avaliable # if：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always

#     host='127.0.0.1',
#     port=3306,
#     user='root',
#     password="",
#     database='website',
#     charset='utf8',
#     cursorclass=pymysql.cursors.DictCursor
# )
# connection = POOL.connection()



connection=pymysql.connect(charset='utf8',db='website',host='127.0.0.1',password="",port=3306,user='root')


app=Flask(__name__,
static_folder="public",
static_url_path="/")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False

app.secret_key= os.urandom(8)

app.config["JWT_SECRET_KEY"] = os.urandom(8)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)


app.register_blueprint(member_manage)
app.register_blueprint(booking_manage)

# Pages
@app.route("/")
def index():
	return rt("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

#%08 issue
@app.route("/api/attractions", methods=["GET"])
def api_attr():
	page=request.args.get("page")
	keyword=request.args.get("keyword")
	print(keyword)
	#got keyword
	if keyword=="undefined":
		keyword=""
	if keyword!=None and keyword != "":
		ender=(int(page)+1)*12
		page=ender-12
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			got=cursor.execute("""SELECT id,name,category2,description,address,transport,mrt,latitude,longitude,images FROM sites WHERE name like %s LIMIT %s,%s """,(("%"+keyword+"%"),page,ender+1))
			result=cursor.fetchall()
			# count=cursor.rowcount
			connection.commit()
			if got != 0:
				summary=[]
				if got<13:
					# s=looper(result)
					for site in result:
						a_set={"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}
						a_set["images"]=ast.literal_eval(a_set["images"])
						summary.append(a_set)
					# print("notfull",s)
					final={"nextPage":None,"data":summary}
					# s=None
				else:
					counter=0
					# s=looper(result)
					for site in result:
						counter+=1
						a_set={"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}
						a_set["images"]=ast.literal_eval(a_set["images"])
						summary.append(a_set)
						if counter==12:
							# print("isfull",s)
							final={"nextPage":int(ender)//12,"data":summary}
							# s=None
							return jsonify(final)
			return jsonify({"error":True,"message":"查無資料"})
	#no keywords
	else:
		if page==None:
			page=0
		#應改為抓13筆 判斷有無下頁
		ender=(int(page)+1)*12
		page=ender-11
		#1,12    13,24    25,36
		print(2,page,ender)
		with connection.cursor(pymysql.cursors.DictCursor) as cursor:
			got=cursor.execute("""SELECT id,name,category2,description,address,transport,mrt,latitude,longitude,images FROM sites WHERE id>=%s AND id<=%s """,(page,ender+1))
			result=cursor.fetchall()
			connection.commit()
			if got != 0:
				counter=0
				summary=[]
				#無下頁
				if got<13:
					# print("looper works")
					# s=looper(result)
					for site in result:
						counter+=1
						a_set={"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}
						a_set["images"]=ast.literal_eval(a_set["images"])
						summary.append(a_set)
					final={"nextPage":None,"data":summary}
					# s=None
					return jsonify(final)
				#有下頁
				else:
					counter=0
					for site in result:
						counter+=1
						a_set={"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}
						a_set["images"]=ast.literal_eval(a_set["images"])
						summary.append(a_set)
						if counter==12:
							final={"nextPage":int(ender)//12,"data":summary}
							print("still going",counter)
							return jsonify(final)
			return jsonify({"error":True,"message":"查無資料"})
		

#單一景點資料
@app.route("/api/attraction/<attractionId>", methods=["GET"])
def api_atid(attractionId):
	with connection.cursor(pymysql.cursors.DictCursor) as cursor:
		got=cursor.execute("""SELECT id,name,category2,description,address,transport,mrt,latitude,longitude,images FROM sites WHERE id=%s""",(attractionId))
		site=cursor.fetchone()
		connection.commit()
		if got!=0:
			summary={"data":{"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}}
			summary["data"]["images"]=ast.literal_eval(summary["data"]["images"])
			return jsonify(summary)
		return jsonify({"error":True,"message":"查無資料"})

#未持token
@jwt.unauthorized_loader
def custom_unauthorized_response(err):
	print("how?: ",err)
	return jsonify({"data":None})
#持有token但過期
@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return jsonify(code="XD", err="Token expired, please login again"), 401


if __name__=="__main__":
	app.run(host='0.0.0.0',port=3000,debug=True)