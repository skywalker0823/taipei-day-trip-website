#會員系統

from urllib import response
from flask import Blueprint, jsonify, request, session
from flask import current_app
from pymysql import *
import pymysql
import os
import sys, traceback
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies

from flask_jwt_extended import jwt_required
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt

from datetime import datetime
from datetime import timedelta
from datetime import timezone


member_manage = Blueprint('member_manage',__name__,template_folder="templates")
connection=pymysql.connect(charset='utf8',db='website',host='127.0.0.1',password="",port=3306,user='root')




#會員總控制 for iden,login,signup
def db(acc,pss,name,att):
	if att=="iden":
		try:
			with connection.cursor(pymysql.cursors.DictCursor) as cursor:
				cursor.execute("""SELECT id,name,username FROM member WHERE username=%s""",(acc,))
				result=cursor.fetchone()
				connection.commit()
				return {"id":result['id'],"name":result['name'],"email":result['username']}
		except Exception as e:
			print("type error: " + str(e))
			print(traceback.format_exc())
	elif att=="login":
		try:
			with connection.cursor(pymysql.cursors.DictCursor) as cursor:
				got=cursor.execute("""SELECT * FROM member WHERE username=%s""",(acc,))
				result=cursor.fetchone()
				connection.commit()
				if got==0:
					return "查無此號"
				elif got==1:
					if pss==result['password']:
						return "ok"
					else:
						return "錯誤的密碼"
				else:
					return "database error"
		except Exception as e:
			print("type error: " + str(e))
			print(traceback.format_exc())
	elif att=="signup":
		try:
			with connection.cursor() as cursor:
				got=cursor.execute("""SELECT * FROM member WHERE username=%s""",(acc,))
				connection.commit()
				if got!=0:
					return "已有相同帳號"
				else:
					with connection.cursor() as cursor:
						result=cursor.execute(
							"""INSERT INTO
							member(
								name,
								username,
								password)
						VALUES(%s,%s,%s)""",(name,acc,pss))
						connection.commit()
						return "ok"
		except Exception as e:
			print("type error: " + str(e))
			print(traceback.format_exc())
	else:
		print('att cannot defined')


#會員系統-茶豬料
#從session 斷定此使用者身份 並回傳該資訊
#session判斷未登入則傳回{"data":"null"}
@member_manage.route('/api/user',methods=['GET'])
@jwt_required()
def iden():
	try:
		acc=get_jwt_identity()
		result=db(acc,None,None,"iden")
		return jsonify({'data':result})
	except Exception as e:
		print("type error: " + str(e))
		print(traceback.format_exc())




#會員系統-註冊
#給予token 並要求重新登入
@member_manage.route("/api/user",methods=['POST'])
def signup():
	try:
		data=request.get_json()
		acc=data['email']
		pss=data['password']
		name=data['name']
		att="signup"
		result=db(acc,pss,name,att)
		if result=="ok":
			return jsonify({result:True})
		return jsonify({"error":result})
	except Exception as e:
		print("type error: " + str(e))
		print(traceback.format_exc())



#會員系統-登入
#確認token 返回姓名 與目前訂位狀況 以及ok 
@member_manage.route("/api/user",methods=['PATCH'])
def login():
	try:
		data=request.get_json()
		acc=data['email']
		pss=data['password']
		name=None
		att="login"
		result=db(acc,pss,name,att)
		#字典類型錯誤!
		if result=="ok":
			# session['user']=acc
			response = jsonify({result:True})
			access_token = create_access_token(identity=acc)
			set_access_cookies(response,access_token)
			return response
		return jsonify({"error":result})
	except Exception as e:
		print("type error: " + str(e))
		print(traceback.format_exc())




#會員系統-登出
@member_manage.route('/api/user',methods=['DELETE'])
def logout():
	try:
		response = jsonify({"ok":True})
		unset_jwt_cookies(response)
		return response
	except Exception as e:
		print("type error: " + str(e))
		print(traceback.format_exc())

#refresh token
@member_manage.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response
