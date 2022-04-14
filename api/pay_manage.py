from unittest import result
from flask import Blueprint, jsonify, request
import os
from modules.db import Pay
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from dotenv import load_dotenv
from datetime import date
import random
import requests,json
import ast

pay_manage = Blueprint('pay_manage',__name__,template_folder="templates")

load_dotenv()

partner_key=os.getenv("partner_key")

@pay_manage.route("/api/orders",methods=["POST"])
@jwt_required()
def order():
    try:
        if request.method=="POST":
            data=request.get_json()
            contacts=data["order"]["contact"]
            print("contact: ",contacts)
            if "@" not in contacts["email"]:
                return jsonify({"error":"email invalid"})
            if contacts["name"]=="" or contacts["phone"]=="":
                return jsonify({"error":"contact data invalid"})
            try:
                int(contacts["phone"])
            except:
                return jsonify({"error":"phone invalid"})
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
            who=get_jwt_identity()
            user_id=who["id"]
            uniq_id=str(date.today().strftime('%Y%m%d'))+str(random.randint(1000,9999))
            total_price=data["order"]["t_price"]
            attractions=data["order"]["trip"]
            contact=contacts
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
            if orderNumber=="all":
                who=get_jwt_identity()
                user_id=who["id"]
                data=Pay.get_all(user_id)
                summary=[]
                for site in data:
                    uniq_id=site["uniq_id"]
                    total=site["total_price"]
                    attractions=ast.literal_eval(site["attractions"])
                    contact=ast.literal_eval(site["contacts"])
                    status=site["status"]
                    summary.append({"uniq_id":uniq_id,"total":total,"attraction":attractions,"contact":contact,"status":status})
                return jsonify(summary)
            data=Pay.check_order(orderNumber)
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
