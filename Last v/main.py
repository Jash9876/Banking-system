from fastapi import FastAPI
from fastapi.responses import JSONResponse
import mysql.connector as s

app = FastAPI()
connection= s.connect(username='Jashwanth',password='Prajas@0106',host='localhost', database='proj1')
cur=connection.cursor()
print(connection.is_connected())

table = 'users'
cur.execute("SHOW TABLES")
results = cur.fetchall()

print('All existing tables:', results)

results_list = [item[0] for item in results] 

if table in results_list:
    print(table, 'was found!')
else:
    print(table, 'was NOT found....Creating now!')
    cur.execute("create table users(Accno int primary key auto_increment,Username varchar(10),password varchar(20),Balance int)")
    connection.commit()

@app.get("/login/{username}/{password}")
def login(username: str, password: str):
    cur.execute("select username from users")
    d=cur.fetchall()
    cur.execute("select password from users where username='{}'".format(username))
    d1=cur.fetchone()
    a=1
    if d1!=None:
        for i in d:
            if i[0]==username:
                if password==d1[0]:
                    a=2
                    break
            else:
                a=3      
    if a==2:
        cur.execute("select balance from users where username='{}' and password='{}'".format(username,password))
        amt=cur.fetchone()[0]
        cur.execute("select accno from users where username='{}' and password='{}'".format(username,password))
        acc=cur.fetchone()[0]
        headers = {"Access-Control-Allow-Origin": "*"}
        return JSONResponse({"bank-balance": amt, "acc-no": acc}, headers=headers)
    elif a==3:
        headers = {"Access-Control-Allow-Origin": "*"}
        return JSONResponse({"bank-balance":401}, headers=headers)
    else:
        headers = {"Access-Control-Allow-Origin": "*"}
        return JSONResponse({"bank-balance":402}, headers=headers)

@app.get("/signup/{username}/{password}")
def signup(username: str, password: str):
    cur.execute("select username from users")
    d=cur.fetchall()
    a=False
    for i in d:
        if username==i[0]:
            a=True
    if a==False:
        cur.execute("insert into users (username,password,balance) values('{}','{}',0)".format(username,password))
        connection.commit()
        cur.execute("select accno from users where username='{}' and password='{}'".format(username,password))
        acc=cur.fetchone()[0]
        data=0
        headers = {"Access-Control-Allow-Origin":"*"}
        return JSONResponse({"bank-balance": data, "acc-no": acc}, headers=headers)
    else:
        headers = {"Access-Control-Allow-Origin": "*"}
        return JSONResponse({"Error":403},headers=headers)

@app.get("/withdraw/{username}/{password}/{amt}")
def withdraw(username: str, password: str, amt: int):
    headers = {"Access-Control-Allow-Origin": "*"}

    cur.execute("select balance from users where username='{}' and password='{}'".format(username,password))
    data=cur.fetchone()[0]
    if data>amt:
        data=data-amt
        cur.execute("update users set balance='{}' where username='{}' and password='{}'".format(data,username,password))
        connection.commit()
        return JSONResponse({"bank-balance": data}, headers=headers)
    else:
        return JSONResponse({"bank-balance": "Not enough funds"}, headers=headers)

@app.get("/deposit/{username}/{password}/{amt}")
def deposit(username: str, password: str, amt: int):
    headers = {"Access-Control-Allow-Origin": "*"}
    cur.execute("select balance from users where username='{}' and password='{}'".format(username,password))
    data=cur.fetchone()[0]
    data=data+amt
    cur.execute("update users set balance='{}' where username='{}' and password='{}'".format(data,username,password))
    connection.commit()
    return JSONResponse({"bank-balance":data}, headers=headers)