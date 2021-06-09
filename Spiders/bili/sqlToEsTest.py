import mysql.connector
from elasticTest import elaticsearch
from datetime import datetime
conn = mysql.connector.connect(user='root',
                               password='emmith',
                               database='test',
                               auth_plugin='mysql_native_password')
mycursor = conn.cursor()
sql = "select * from `estest`"
mycursor.execute(sql)
res = mycursor.fetchall()
print(res, type(res))
mycursor.close()
conn.close()

es = elaticsearch(index_name='spider',index_type="spider_data")
es.create_index
for i in res:
    data = {
        'title': i[0],
        'content': i[1],
        'link': i[2],
        'create_time': datetime.now()
    }

    es.insert_one(doc=data)