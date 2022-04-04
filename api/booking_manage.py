import re
from flask import Blueprint, jsonify, request
import jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from modules.db import Book


booking_manage = Blueprint('booking_manage',__name__,template_folder="templates")


#get 尚未確認下單的預定行程資料，null 表示沒有資料
###未登入或有錯誤回覆{"error": true,"message": "自訂的錯誤訊息"}
@booking_manage.route('/api/booking',methods=['GET','POST','DELETE'])
@jwt_required()
def booker():
    if request.method=="GET":
        try:
            who=get_jwt_identity()
            id=who["id"]
            result=Book.book_get(id)
            return jsonify(result)
        except Exception as e:
            print("錯誤:",e)
        finally:
            print("Booking!")

    elif request.method=="POST":
        try:
            print("post!")
            who=get_jwt_identity()
            result=Book.book_post(who)
            return jsonify(result)
        except:
            return jsonify({"error":True,"message":"建立行程失敗"})

    elif request.method=="DELETE":
        try:
            data=request.get_json()
            id=data['id']
            result=Book.book_del(id)
            return jsonify(result)
        except Exception as e:
            print("type error: " + str(e))
    else:
        return None