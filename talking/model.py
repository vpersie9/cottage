__author__ = 'vpersie9'
#-*-coding:utf-8-*-
import MySQLdb
def connection():
    conn = MySQLdb.connect('localhost','root','199099','test',charset='utf8')
    return conn

connect = connection()
cursor = connect.cursor()

def send(info, sender, datetime):
    try:
        sql="insert into communication (info,sender,datetime) values ('%s','%s','%s')"%(info,sender,datetime)
        cursor.execute(sql)
        connect.commit()
    except Exception,e:
        return e

def show():
    sql="select * from communication"
    cursor.execute(sql)
    result=cursor.fetchall()
    connect.commit()
    all=[]
    for each in result:
        all.append(each[1:])
    return all
