from pymysql import connect

conn = connect(
    host='localhost',
               port=3306, user='fancy',
               password='sf825874',
               database='my_stock',
               charset='utf8')

cs = conn.cursor()
cs.execute("select * from info;")
my_stock_info = cs.fetchall()

cs.close()
conn.close()

print(str(my_stock_info))

# content = re.sub(r"\{%content%\}", str(my_stock_info), content)
