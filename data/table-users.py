# import pymysql
# import os

# def build(conn):
#     cursor.execute("DROP TABLE IF EXISTS users")
#     sql = """CREATE TABLE sites(
#         id MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#         name varchar(255) NOT NULL,
#         category varchar(255),
#         category2 varchar(255),
#         description TEXT,
#         address varchar(255),
#         transport TEXT,
#         mrt varchar(255),
#         latitude varchar(255),
#         longitude varchar(255),
#         images TEXT
#     )"""
#     cursor.execute(sql)
#     conn.commit()


# if __name__=="__main__":
#     conn=pymysql.connect(charset='utf8',db='website',host='127.0.0.1',password="",port=3306,user='root')
#     cursor=conn.cursor()
#     build(conn)
#     cursor.close()