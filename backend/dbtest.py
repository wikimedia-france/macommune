import pymysql
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.my.cnf'))

db_user = config['client']['user']
db_password = config['client']['password']
db_host = 'localhost'
db_name = 'ma_commune'


conn = pymysql.connect(host=db_host,
                       port=3306,
                       user=db_user,
                       passwd=db_password,
                       db=db_name)

cur = conn.cursor()

dept = 93
cur.execute("SELECT * FROM communes WHERE insee LIKE '{}%';".format(dept))

print(cur.description)

for row in cur:
    print(row)

cur.close()
conn.close()
