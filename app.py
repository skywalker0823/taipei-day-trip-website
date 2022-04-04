# from dotenv import load_dotenv
from flask import *
import os
from flask import render_template as rt
from modules.looper import looper
from api.att_manage import att_manage
from api.member_manage import member_manage
from api.booking_manage import booking_manage
from api.pay_manage import pay_manage
from flask_jwt_extended import JWTManager
from datetime import timedelta

app=Flask(__name__,static_folder="static",static_url_path="/")

#config務必另外寫
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False
app.config["JWT_SECRET_KEY"] = os.urandom(8)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.secret_key= os.urandom(8)

jwt = JWTManager(app)

app.register_blueprint(att_manage)
app.register_blueprint(member_manage)
app.register_blueprint(booking_manage)
app.register_blueprint(pay_manage)

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
	app.run(host='0.0.0.0',port=3000)