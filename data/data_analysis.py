import json
import pymysql
import os
from dotenv import load_dotenv
datas=open("taipei-attractions.json")
datas_json=json.load(datas)

#創立table
def build(conn):
    cursor.execute("DROP TABLE IF EXISTS sites")
    sql = """CREATE TABLE sites(
        id MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name varchar(255) NOT NULL,
        category varchar(255),
        category2 varchar(255),
        description TEXT,
        address varchar(255),
        transport TEXT,
        mrt varchar(255),
        latitude varchar(255),
        longitude varchar(255),
        images TEXT
    )"""
    cursor.execute(sql)
    conn.commit()


#輸入資料
def insert_data(conn):
            with conn.cursor() as cursor:
                sites=datas_json["result"]["results"]
                for site in sites:
                    images=[]
                    pics=site["file"].lower().split("jpg")
                    name=site["stitle"]
                    cat1=site["CAT1"]
                    cat2=site["CAT2"]
                    des=site["xbody"]
                    add=site["address"]
                    trans=site["info"]
                    mrt=site["MRT"]
                    lati=site["latitude"]
                    longi=site["longitude"]
                    for pic in pics:
                        if pic.endswith("."):
                            img=pic+"jpg"
                            images.append(img)
                    result=cursor.execute(
                        """INSERT INTO
                            sites(
                                name,
                                category,
                                category2,
                                description,
                                address,
                                transport,
                                mrt,
                                latitude,
                                longitude,
                                images
                                )
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(name,cat1,cat2,des,add,trans,mrt,lati,longi,str(images)))
                    conn.commit()
                    print("完成 新增: ",result,"筆資料",images)



if __name__=="__main__":
    load_dotenv()
    conn=pymysql.connect(charset='utf8',db='website',host='127.0.0.1',password=os.getenv("DB_PASS"),port=3306,user='root')
    cursor=conn.cursor()
    build(conn)
    insert_data(conn)
    cursor.close()
    datas.close()