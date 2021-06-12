import mysql.connector
from .items import DyttItem
conn = mysql.connector.connect(user='root',
                               password='emmith',
                               database='test',
                               auth_plugin='mysql_native_password')
mycursor = conn.cursor()
item = DyttItem()
item['title']='风筝在阴天搁浅'
item['category']='wrj'
item['download_url']='100'

sql = "insert into `dytt` (`title`,`category`,`download_url`) values ('%s','%s','%s')" % \
(item['title'],item['category'],item['download_url'])
mycursor.execute(sql)
conn.commit()
conn.close