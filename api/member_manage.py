#會員系統
from urllib import response
from flask import Blueprint, jsonify, request, session
from flask import current_app
from modules.db import Member
import os
import sys, traceback
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import jwt_required
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from datetime import date, datetime
from datetime import timedelta
from datetime import timezone


member_manage = Blueprint('member_manage',__name__,template_folder="templates")


#會員系統-茶豬料
#從session 斷定此使用者身份 並回傳該資訊
@member_manage.route('/api/user',methods=['GET'])
@jwt_required()
def iden():
	try:
		print("acquired!")
		acc=get_jwt_identity()
		result=Member.db(acc["acc"],None,None,"iden")
		return jsonify({'data':result})
	except Exception as e:
		print("type error: " + str(e))
		print(traceback.format_exc())



#會員系統-註冊
#給予token 並要求重新登入
@member_manage.route("/api/user",methods=['POST'])
def signup():
	try:
		#需要檢查{email:acc,password:pss,name:name}
		data=request.get_json()
		acc=data['email']
		pss=data['password']
		name=data['name']
		if "@" in acc and pss != "" and name != "":
			att="signup"
			result=Member.db(acc,pss,name,att)
			if result=="ok":
				return jsonify({result:True})
			return jsonify({"error":result})
		else:
			return jsonify({"error":"signup input errors"})
	except Exception as e:
		print("type error: " + str(e))
		print(traceback.format_exc())



#會員系統-登入
#確認token 返回姓名 與目前訂位狀況 以及ok 
@member_manage.route("/api/user",methods=['PATCH'])
def login():
	try:
		#需要檢查
		data=request.get_json()
		acc=data['email']
		pss=data['password']
		if "@" in acc and pss != "":
			name=None
			att="login"
			result=Member.db(acc,pss,name,att)
			#字典類型錯誤!
			if result[0]=="ok":
				response = jsonify({result[0]:True})
				meta={"acc":acc,"id":str(result[1])}
				access_token = create_access_token(identity=meta)
				set_access_cookies(response,access_token)
				return response
			return jsonify({"error":result})
		else:
			return jsonify({"error":"Login input error"})
	except Exception as e:
		print("type error: " + str(e))
		print(traceback.format_exc())


#會員系統-更改
@member_manage.route('/api/user',methods=['PUT'])
@jwt_required()
def alter():
	try:
		acc=get_jwt_identity()
		data=request.get_json()

		if data["for"]=="name":
			new=data["new_name"]
			if new=="":
				return jsonify({"error":"name none"})
			result=Member.db(acc["acc"],None,new,"PUT")
			if result=="ok":
				return jsonify({"ok":True,"name":new})
			else:
				return jsonify({"error":"Change name error"})
		elif data["for"]=="password":
			new=data["new_pass"]
			if new=="":
				return jsonify({"error":"name none"})
			result=Member.db(acc["acc"],new,None,"PUT")
			print(result)
			if result=="ok":
				return jsonify({"ok":True})
			else:
				return jsonify({"error":"Change password error"})
		else:
			print('PUT request ERROR')

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
