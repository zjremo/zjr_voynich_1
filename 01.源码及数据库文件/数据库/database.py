import pymysql
import csv


# 建立与数据库的连接
def connect_db(connection, file_path, table):
    # 创建游标对象
    cursor = connection.cursor()
    # 打开CSV文件并读取内容
    csv_file = open(file_path, 'r', encoding='UTF-8')
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    # 迭代读取CSV文件中的每一行，并执行插入操作
    for row in csv_reader:
        # 构造插入语句
        query = " "
        if table == "assi":
            query = "INSERT INTO assi (name, que, ans) VALUES ('{}', '{}', '{}')".format(row[0], row[1], row[2])
        # if table == "house":
        # query = "INSERT INTO house VALUES ('{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}')"
        # .format( row[0], row[1], row[2],row[3], row[4], row[5],row[6], row[7], row[8],row[9], row[10], row[11])
        if table == "house":
            query = (
                "INSERT INTO house "
                "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                .format(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]
                )
            )
        cursor.execute(query)
        # 将CSV行中的数据作为参数传递给插入语句

        # 提交事务和关闭连接
        connection.commit()
    connection.close()


# 声明主程序入口
if __name__ == '__main__':
    assi_pa = "E:\\python\\pycharm\\projects\\pythonProject1\\house\\assistant_info_out.csv"
    house_pa = "E:\\python\\pycharm\\projects\\pythonProject1\\house\\house_info.csv"
    connect = pymysql.connect(
        host='localhost',
        user='root',
        password='yxfYXF20030927',
        db='assistance_info'
    )
    connect_db(connect, assi_pa, "assi")
    connect_db(connect, house_pa, "house")
