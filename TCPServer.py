import mysql.connector
from sshtunnel import SSHTunnelForwarder
import pymysql
import MySQLdb

server = SSHTunnelForwarder(
    ("118.31.17.95", 22),
    ssh_password="WangXue960512",
    ssh_username="root",
    remote_bind_address=("172.16.89.15", 3306))
server.start()
# print(server)
mydb = MySQLdb.connect(
    host="127.0.0.1",
    port=server.local_bind_port,
    user="root",
    password="WangXue960512",
    database="cet",
    charset="utf8"
)

#mydb = pymysql.connect("localhost", "root", "root", "cet")