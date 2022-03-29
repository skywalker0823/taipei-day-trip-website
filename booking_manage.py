import re
from flask import Blueprint, jsonify, request
import jwt
import ast
from pymysql import *
import pymysql
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity


booking_manage = Blueprint('booking_manage',__name__,template_folder="templates")


connection=pymysql.connect(charset='utf8',db='website',host='127.0.0.1',password="",port=3306,user='root')

#get 尚未確認下單的預定行程資料，null 表示沒有資料
###未登入或有錯誤回覆{"error": true,"message": "自訂的錯誤訊息"}
@booking_manage.route('/api/booking',methods=['GET','POST','DELETE'])
@jwt_required()
def booker():
    if request.method=="GET":
        #成功給予預定資料 沒資料回null
        #先取得該使用者orders全部資料
        #接下來從景點id先去取一次景點必須資料id name add image(第一張就好)
        #以上兩者整合之後回傳
        try:
            who=get_jwt_identity()
            print(who["id"])
            id=who["id"]
            with connection.cursor() as cursor:
                cursor.execute("""SELECT product,order_id FROM orders WHERE id=%s""",(id,))
                result=cursor.fetchall()
                connection.commit()
                print(result)
                data=[]
                for one_trip in result:
                    true_id=one_trip[1]
                    one_trip=one_trip[0].split("_")
                    site_id=one_trip[0]
                    t_date=one_trip[1]
                    t_price=one_trip[2]
                    if t_price=="2000":
                        t_time="morning"
                    else:
                        t_time="afternoon"
                    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                        cursor.execute("""SELECT name,address,images FROM sites WHERE id=%s""",(site_id,))
                        result=cursor.fetchone()
                        connection.commit()
                        t_summary={"attraction":{"id":site_id,"true_id":true_id,"name":result['name'],"address":result['address'],"image":ast.literal_eval(result['images'])[0]},"date":t_date,"time":t_time,"price":t_price}
                        data.append(t_summary)
                print("終局",data)#此為所有預定資料
                return jsonify({"data":data})
        except Exception as e:
            print("錯誤:",e)
        finally:
            print("Booking!")
    elif request.method=="POST":
        try:
            #成功建立預定資料
            print("post!")
            #此處已確認登入
            who=get_jwt_identity()
            with connection.cursor() as cursor:
                cursor.execute("""SELECT id FROM member WHERE username=%s""",(who['acc'],))
                id=cursor.fetchone()
                connection.commit()
                data=request.get_json()
                site=data["attractionId"]
                date=data["date"]
                de=data["price"]
                meta=site+"_"+date+"_"+de
                print(meta)
                # 進訂單資料庫=會員id 景點預定資料
                with connection.cursor() as cursor:
                    print("正在輸入預定資料")
                    result=cursor.execute(
                        """INSERT INTO
                        orders(
                            id,
                            product)
                        VALUES(%s,%s)
                        """,(id[0],meta))
                    connection.commit()
                    return jsonify({"ok":True})
        except:
            return jsonify({"error":True,"message":"建立行程失敗"})


    elif request.method=="DELETE":
        #成功刪除預定資料回覆ok true
        try:
            data=request.get_json()
            id=data['id']
            with connection.cursor() as cursor:
                cursor.execute("""DELETE FROM orders WHERE order_id=%s""",(id,))
                connection.commit()
                return jsonify({"ok":True})
        except Exception as e:
            print("type error: " + str(e))
    else:
        return None