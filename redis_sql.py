import pymysql
import redis
from rediscluster import StrictRedisCluster

# pool = redis.ConnectionPool(host='10.10.1.77', port=7004)
# pool = redis.ConnectionPool(host='10.10.1.57', port=7001)
startup_nodes = [
            {'host': '10.10.1.57', 'port': '7001'},
            {'host': '10.10.1.57', 'port': '7002'},
            {'host': '10.10.1.57', 'port': '7003'},
            {'host': '10.10.1.77', 'port': '7004'},
            {'host': '10.10.1.77', 'port': '7005'},
            {'host': '10.10.1.77', 'port': '7006'},
        ]
        # 构建StrictRedisCluster对象
r = StrictRedisCluster(startup_nodes=startup_nodes,decode_responses=True)


def connect_db():
	return pymysql.connect(host='localhost',port=3326,user='root',password='2019',database='test')

def query_name(_id):
	sql_str = ("SELECT name" + " FROM friends"+ " WHERE id='%s'" % (_id))
	con = connect_db()
	cur = con.cursor()
	cur.execute(sql_str)
	rows = cur.fetchall()
	cur.close()
	con.close()
	print('='*50)
	print('select from SQL')
	print('='*50)
	return rows[0][0]

def write_redis(n1,n2):
	r.set(n1, n2)
	print('='*50)
	print('write into redis')
	print('='*50)

def get_redis(n1):
	print('='*50)
	print('get from redis')
	print('='*50)
	name = str(r.get(n1))
	if name != 'None':
		print(name)
		return True
	else:
		print('not in redis')
		return False

while True:
	search = int(input("input:"))
	if search > 10:
		status = get_redis(search)
		if status == False:
			print('!!!!!!!!!!!')
			name = query_name(search)
			write_redis(search,name)
	else:
		print(query_name(search))

