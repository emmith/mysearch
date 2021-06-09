import mysql.connector
from bili.items import BiliItem
conn = mysql.connector.connect(user='root',
                               password='emmith',
                               database='test',
                               auth_plugin='mysql_native_password')
mycursor = conn.cursor()
item = BiliItem()
item['name']='风筝在阴天搁浅'
item['author']='wrj'
item['score']='100'
item['rank']='100'
item['playVolume']='100万'

sql = "insert into `bili_rank` (`rank`,`name`,`score`) values ('%s','%s','%s')" % \
(item['rank'],item['name'],item['score'])
mycursor.execute(sql)
conn.commit()