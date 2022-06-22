import pymysql
from dbutils.pooled_db import PooledDB
import sys, traceback
import ast
from flask import request
import os
from dotenv import load_dotenv
from datetime import datetime
from dateutil.parser import parse
#DB密碼config
# from config import Config_AWS
# from instance import config
# password=Config_AWS.DB_PASS
# password=config.DB_PASS

load_dotenv()
POOL = PooledDB(
    creator=pymysql,  # Which DB module to use
    maxconnections=6,  # Allowed max connection, 0 and None means no limitations.
    mincached=2,  # Least connection when created, 0 means don't.
    blocking=True,  # Queue when there is no connection avaliable. True = wait；False = No waits, and report error.
    ping=0, # Check if Mysql service is avaliable # if：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always

    host=os.getenv("DB_host"),
    port=3306,
    user='root',
    password=os.getenv("DB_pass"),
    database='website',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)
connection = POOL.connection()



#資料庫-付費相關
class Pay:
    def create_order(user_id,uniq_id,total_price,attractions,contacts,status):
        print('進資料庫前',user_id,uniq_id,total_price,attractions,contacts,status)
        try:
            with connection.cursor() as cursor:
                result=cursor.execute(
                    """INSERT INTO
                    pay(
                        user_id,
                        uniq_id,
                        total_price,
                        attractions,
                        contacts,
                        status
                    )
                    VALUES(%s,%s,%s,%s,%s,%s)
                    """,(user_id,uniq_id,total_price,attractions,contacts,status))
                connection.commit()
                print("Pay資料庫新增",result)
                return
        except Exception as e:
            print(e)
            print("pay新增CREATE資料錯誤")
            return None
    def check_order(id):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT * FROM pay
                    WHERE uniq_id=%s
                    """,(id)
                )
                result=cursor.fetchone()
                connection.commit()
                return result
        except:
            print("GET PAY資料庫問題")
            return
    def change_order(user_id,target,do_what):
        if do_what=="UPDATE":
            try:
                with connection.cursor() as cursor:
                    result=cursor.execute(
                        """UPDATE pay
                        SET status=0 
                        WHERE uniq_id=%s 
                        """,(target)
                    )
                    connection.commit()
                    print("資料庫pay更新完成",result)
                    return
            except:
                return
        elif do_what=="DELETE":
            try:
                with connection.cursor() as cursor:
                    result=cursor.execute(
                        """DELETE FROM orders
                        WHERE id=%s
                        """,(user_id)
                    )
                    connection.commit()
                    print("已付訂單pay刪除完成",result,"筆")
                    return
            except:
                return
        return
    def get_all(user_id):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT uniq_id,total_price,attractions,contacts,status FROM pay WHERE user_id=%s""",(user_id,))
                result=cursor.fetchall()
                connection.commit()
                return result
        except:
            print("get all error")



#資料庫-會員管理
class Member:
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
                            id=result['id']
                            return ("ok",id)
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

        elif att=="PUT":
            if name:
                try:
                    with connection.cursor() as cursor:
                        print(name,acc)
                        got=cursor.execute("""UPDATE member SET name=%s WHERE username=%s""",(name,acc))
                        connection.commit()
                        if got!=0:
                            return "ok"
                        else:
                            return "error"
                except Exception as e:
                    print("type error: " + str(e))
                    print(traceback.format_exc())
            elif pss:
                try:
                    with connection.cursor() as cursor:
                        print(pss,acc)
                        got=cursor.execute("""UPDATE member SET password=%s WHERE username=%s""",(pss,acc))
                        connection.commit()
                        if got!=0:
                            return "ok"
                        else:
                            return "error"
                except Exception as e:
                    print("type error: " + str(e))
                    print(traceback.format_exc())
            else:
                print("db change profile failure")
        else:
            print('att cannot defined')

#資料庫-景點
class Attraction:
    def attraction_key(page,ender,keyword):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            got=cursor.execute("""SELECT id,name,category2,description,address,transport,mrt,latitude,longitude,images FROM sites WHERE name like %s LIMIT %s,%s """,(("%"+keyword+"%"),page,ender+1))
            result=cursor.fetchall()
            connection.commit()
            if got != 0:
                summary=[]
                if got<13:
                    for site in result:
                        a_set={"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}
                        a_set["images"]=ast.literal_eval(a_set["images"])
                        summary.append(a_set)
                        final={"nextPage":None,"data":summary}
                        return final
                else:
                    counter=0
                    for site in result:
                        counter+=1
                        a_set={"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}
                        a_set["images"]=ast.literal_eval(a_set["images"])
                        summary.append(a_set)
                        if counter==12:
                            final={"nextPage":int(ender)//12,"data":summary}
                            return final
            return ({"error":True,"message":"查無資料"})
    def attraction_no_key(page,ender):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            got=cursor.execute("""SELECT id,name,category2,description,address,transport,mrt,latitude,longitude,images FROM sites WHERE id>=%s AND id<=%s """,(page,ender+1))
            result=cursor.fetchall()
            connection.commit()
            if got != 0:
                counter=0
                summary=[]
                if got<13:
                    for site in result:
                        counter+=1
                        a_set={"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}
                        a_set["images"]=ast.literal_eval(a_set["images"])
                        summary.append(a_set)
                    final={"nextPage":None,"data":summary}
                    return final
                else:
                    counter=0
                    for site in result:
                        counter+=1
                        a_set={"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}
                        a_set["images"]=ast.literal_eval(a_set["images"])
                        summary.append(a_set)
                        if counter==12:
                            final={"nextPage":int(ender)//12,"data":summary}
                            print("still going",counter)
                            return final
            return ({"error":True,"message":"查無資料"})
    def attraction_id(attractionId):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            got=cursor.execute("""SELECT id,name,category2,description,address,transport,mrt,latitude,longitude,images FROM sites WHERE id=%s""",(attractionId))
            site=cursor.fetchone()
            connection.commit()
            if got!=0:
                summary={"data":{"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}}
                summary["data"]["images"]=ast.literal_eval(summary["data"]["images"])
                return summary
            return ({"error":True,"message":"查無資料"})


#資料庫-預定相關

class Book:
    def book_get(id):
            with connection.cursor() as cursor:
                cursor.execute("""SELECT product,order_id FROM orders WHERE id=%s""",(id,))
                result=cursor.fetchall()
                connection.commit()
                data=[]
                for one_trip in result:
                    true_id=one_trip['order_id']
                    one_trip=one_trip['product'].split("_")
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
                return ({"data":data})

    def book_post(who):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT id FROM member WHERE username=%s""",(who['acc'],))
                id=cursor.fetchone()
                connection.commit()
                data=request.get_json()
                #{ attractionId: site, date: date, time: time,price:price }
                site=data["attractionId"]
                date=data["date"]#必須是今天之後

                #日期檢查區-格式滿足&日期需>=今日
                parse(date)
                dateformatter="%Y-%m-%d"
                checker=datetime.strptime(date,dateformatter)
                today=datetime.now()

                if checker>=today:
                    cost=data["price"]
                    if cost=="2500" or cost=="2000":
                        if site!="" and date!="":
                            print("book pass")
                            meta=site+"_"+date+"_"+cost
                            # 進訂單資料庫=會員id 景點預定資料
                            with connection.cursor() as cursor:
                                result=cursor.execute(
                                    """INSERT INTO
                                    orders(
                                        id,
                                        product)
                                    VALUES(%s,%s)
                                    """,(id["id"],meta))
                                connection.commit()
                                return ({"ok":True})
                        else:
                            return ({"error":"book_post input error"})
                    else:
                        return ({"error":"input COST error"})
                else:
                    return({"error":"date is not allowed"})
        except Exception as e:
                print("type error: " + str(e))
                print(traceback.format_exc())

    def book_del(id):
            with connection.cursor() as cursor:
                cursor.execute("""DELETE FROM orders WHERE order_id=%s""",(id,))
                connection.commit()
                return ({"ok":True})















# class Order:
#     def setPo(email,poNumber,price,prime,attraction_id,po_date,po_time,phone):
#         try:
#             connect_pool=pool.get_connection()
#             mycursor = connect_pool.cursor()
#             mycursor.execute("SELECT user_id from users where email=%s",(email,))
#             user_id=mycursor.fetchone()[0]
#             sql = ("INSERT INTO bookinginfo(po,price,prime,attraction_id,date,time,user_id,phone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
#             val = (poNumber,price,prime,attraction_id,po_date,po_time,user_id,phone)
#             mycursor.execute(sql, val)
#             connect_pool.commit()
#             connect_pool.close()
#         except Exception as e:
#             connect_pool.close()
#             print(f"儲存資料錯誤: {e}")
#             return