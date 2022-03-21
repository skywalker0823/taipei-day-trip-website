import re
from flask import Blueprint, jsonify, request
from pymysql import *
import pymysql


booking_manage = Blueprint('booking_manage',__name__,template_folder="templates")


connection=pymysql.connect(charset='utf8',db='website',host='127.0.0.1',password="",port=3306,user='root')


#get 尚未確認下單的預定行程資料，null 表示沒有資料
@booking_manage.route('/api/booking',methods=['GET','POST','DELETE'])
def booker():
    if request.method=="GET":
        return None
    elif request.method=="POST":
        return None
    elif request.method=="DELETE":
        return None
    else:
        return None