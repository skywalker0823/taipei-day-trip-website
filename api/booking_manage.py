

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from modules.db import Book

booking_manage = Blueprint('booking_manage',__name__,template_folder="templates")

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
            return jsonify({"error":True,"message":"取得行程失敗"})
        finally:
            print("Get Booking!")


    elif request.method=="POST":
        try:
            print("post!")
            who=get_jwt_identity()
            result=Book.book_post(who)
            return jsonify(result)
        except Exception as e:
            print("錯誤:",e)
            return jsonify({"error":True,"message":"建立行程失敗"})
        finally:
            print("Post Booking!")

            
    elif request.method=="DELETE":
        try:
            data=request.get_json()
            id=data['id']
            result=Book.book_del(id)
            return jsonify(result)
        except Exception as e:
            print("錯誤",e)
            return jsonify({"error":True,"message":"刪除行程失敗"})
        finally:
            print("Delete Booking!")
    else:
        return None