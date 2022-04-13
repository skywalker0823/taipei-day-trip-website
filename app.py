# from dotenv import load_dotenv
from flask import *
from flask import render_template as rt
from api.att_manage import att_manage
from api.member_manage import member_manage
from api.booking_manage import booking_manage
from api.pay_manage import pay_manage
from flask_jwt_extended import JWTManager
from config import Config_AWS

app=Flask(__name__,static_folder="static",static_url_path="/",instance_relative_config=True)

app.config.from_object(Config_AWS)
#local configs
# app.config.from_pyfile('config.py')

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
@app.route("/member")
def member():
	return render_template("member.html")


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
	app.run(host="0.0.0.0",port=3000)