from unittest import result
from flask import Blueprint, jsonify, request
import os
from modules.db import Pay
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
# from dotenv import load_dotenv
from datetime import date
import random
import requests,json
import ast

pay_manage = Blueprint('pay_manage',__name__,template_folder="templates")

# load_dotenv()
partner_key="partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM"


#建立訂單POST
#jwt中塞有使用者id及mail了
#彙整資料庫所需資料 一次打進資料庫中
#將會是一個很複雜的JSON
@pay_manage.route("/api/orders",methods=["POST"])
@jwt_required()
def order():
    try:
        if request.method=="POST":
            #自前端取得資料 並且主動至tappay比對訊息
            data=request.get_json()
            contacts=data["order"]["contact"]
            to_tappay={
                "prime":data["prime"],
                "partner_key":partner_key,
                "merchant_id":"GlobalTesting_CTBC",
                "details":"這裏可放置訂單資訊",
                "amount":data["order"]["t_price"],
                "cardholder":{
                    "phone_number":contacts["phone"],
                    "name":contacts["name"],
                    "email":contacts["email"],
                    "zip_code":"",
                    "address":"",
                    "national_id":"",
                },
                "remember":True
            }
            #送出前資料檢查站
            if contacts["phone"]=="" or contacts["name"]=="" or contacts["email"]=="":
                return jsonify({"error":True,"message":"個人資料不完整"})
            #資料進資料庫
            #應含有:0.使用者id 1.特殊時間訂單編號 2.總價格 3.景點們 4.聯絡方式 5.狀態碼1尚未付款
            who=get_jwt_identity()
            user_id=who["id"]
            #時間加亂碼產生
            uniq_id=str(date.today().strftime('%Y%m%d'))+str(random.randint(1000,9999))
            total_price=data["order"]["t_price"]
            attractions=data["order"]["trip"]#此項目是陣列 務必注意處理方式
            contact=contacts#此項目為字典 注意處理方式
            status=1#0為已付款 1為待付款
            Pay.create_order(user_id,uniq_id,total_price,str(attractions),str(contact),status)

            #tappay request確認付款
            url="https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
            result=requests.post(url,headers={
                "Content-Type":"application/json",
                "x-api-key":partner_key
            },data=json.dumps(to_tappay))
            result=result.json()
            if result["status"]==0:
                #付款成功 刪除orders資料庫中資料 保留pay資料但改變狀態碼為0付款成功
                Pay.change_order(user_id,uniq_id,"UPDATE")
                Pay.change_order(user_id,uniq_id,"DELETE")
                return jsonify({
                    "data":{
                    "number":uniq_id,
                    "payment":{
                        "status":result['status'],
                        "message":"付款成功"
                    }
                }})
            else:
                #付款失敗 保留兩者資料
                return jsonify({
                    "data":{
                    "number":uniq_id,
                    "payment":{
                        "status":result['status'],
                        "message":"付款斯拜"
                    }
                }})
        else:
            print("--something bad at order--")
    except Exception as e:
        print(e)
        return jsonify({"error":True,"message":"order資料庫錯誤"})
    finally:
        print("order!")

@pay_manage.route("/api/orders/<orderNumber>",methods=["GET"])
@jwt_required()
def order_get(orderNumber):
    try:
        if request.method=="GET":
            #依據訂單號碼回傳查詢的訂單
            #抓路徑尾編號為查詢依據

            data=Pay.check_order(orderNumber)
            #此data為一龐大混合資料
            print("GET PAY",data)
            summary={
                "data":{
                "number":data["uniq_id"],
                "price":data["total_price"],
                "trip":ast.literal_eval(data["attractions"]),
                "contact":ast.literal_eval(data["contacts"]),
                "status":data["status"]
                }
            }
            print(summary)
            return jsonify(summary)
        else:
            print("--something bad at order--")
    except Exception as e:
        print(e)
        return jsonify({"error":True,"message":"order資料庫錯誤"})
    finally:
        print("order!")