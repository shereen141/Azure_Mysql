import os

import mysql.connector
import time
from flask import Flask, render_template

app = Flask(__name__)

def dbconnect():

    return mysql.connector.connect(user= , password= , host="mysqlshereen.mysql.database.azure.com", port=3306, database='test')

@app.route('/result', methods=['POST', 'GET'])
def query():
    start_time = time.time()
    display = []
    conn=dbconnect()
    curr=conn.cursor()
    curr.execute("""
UPDATE TABLE SET columnName = null WHERE YourCondition
delete from FOOD where DIGITS >900;""")

    sql=curr.fetchall()

    for row in sql:
        tuple = (row[0], row[1], row[3])
        display.append(tuple)
    end_time = time.time()
    total_time = end_time - start_time
    print("final time:", total_time)
    display.append(total_time)
    curr.close()
    conn.close()
    return render_template('display.html', display=display)


@app.route('/download', methods=['POST', 'GET'])
def download():
    list = []
    if request.method == 'POST':
        mytext = request.form['text1']
        mytext1 = request.form['text2']
        conn = dbconnect()
        curr = conn.cursor()
        r1=int(mytext)
        r2 = int(mytext1)
        curr.execute('select DIGITS,CATEGORY from food DIGITS ">"' +r1+'DIGITS"<"'+r2)
        sql = curr.fetchall()
        #curr.execute('select PICTURE from FOOD')
        data = curr.fetchone()[0]
        for row in data:
            with open('/home/shereen/quiz8/static/'+name+'.jpg','w') as local_file:
                local_file.write(data)
            list.append(data)
        #img_name = name+'.jpg'

    curr.close()
    conn.close()
    #return img_name
    return render_template('result.html',list=list,)


def insert():
    conn = dbconnect()
    curr = conn.cursor()
    path = '/home/shereen/quiz8/data/'

    for root, dirs, files in os.walk('/home/shereen/quiz8/data/'):
        for file in files:
            img_file = file.replace('csv', 'jpg')
            print(img_file)
            if file.endswith(".csv"):
                with open(path + file) as f:
                    name = file[:-4]
                    lines = f.readlines()
                    line1 = lines[0].replace('\r', '')
                    line2 = lines[1].replace('\r', '')
                    line3 = lines[2].replace('\r', '')
                    with open('/home/shereen/quiz8/data/' + img_file, 'rb') as img:
                        image = img.read()
                    sql = 'insert into FOOD (NAME,ingred,digits,category,picture) values (%s,%s,%s,%s,%s)'
                    args = (name,line2, line1, line3, image)
                    curr.execute(sql, args)
                    conn.commit()

def dbcount():
    print('hi')
    conn = dbconnect()
    cur = conn.cursor()
    start_time = time.time()
    conn = dbconnect()
    cur = conn.cursor()
    quer = 'select count(*) from FOOD'
    cur.execute(quer)
    res = cur.fetchone()
    print(res[0])
    conn.commit()
    cur.close()
    conn.close()
    end_time = time.time()
    tot = end_time - start_time
    cur.close()
    conn.close()
    return res

@app.route('/')
def hello_world():
    insert()
    #query()
    img_name = download()
    #return render_template('result.html', img_name=img_name)
    return render_template('main.html')


if __name__ == '__main__':
    app.run()
