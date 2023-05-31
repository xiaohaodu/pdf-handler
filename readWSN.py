import pymysql


def readWSN():
    with open('WSN-判断题.txt', 'r', encoding='utf-8') as txt:
        txt = txt.readlines()
    for i, v in enumerate(txt):
        if txt[i].isspace():
            del txt[i]
        txt[i] = txt[i].replace('\n', '')
    txt = [txt[i:i + 4] for i in range(0, len(txt), 4)]
    for i in range(0, len(txt)):
        txt[i][3] = txt[i][3][-1]
    # 创建数据库连接
    conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="187139", db="mayuan")
    # 获取一个游标对象
    cursor = conn.cursor()
    # 设置参数i，for语句循环
    cursor.execute("delete from questionbank where book='无线传感器网络' and chapter='判断题'")
    cursor.execute("alter table questionbank auto_increment 1")
    for i in range(0, len(txt)):
        param = txt[i]
        sql = "insert into questionbank(book,chapter,question_type,question,selectA,selectB,isSelect) values('无线传感器网络','判断题','判断题',%s,%s,%s,%s)"
        cursor.execute(sql, param)
    # 提交到数据库执行
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()


def readWSN2():
    with open('WSN-选择题.txt', 'r', encoding='utf-8') as txt:
        txt = txt.readlines()
    for i, v in enumerate(txt):
        if txt[i].isspace():
            del txt[i]
        txt[i] = txt[i].replace('\n', '')
    txt = [txt[i:i + 6] for i in range(0, len(txt), 6)]
    for i in range(0, len(txt)):
        txt[i][-1] = txt[i][-1][-1]
    # 创建数据库连接
    conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="187139", db="mayuan")
    # 获取一个游标对象
    cursor = conn.cursor()
    # 设置参数i，for语句循环
    cursor.execute("delete from questionbank where book='无线传感器网络' and chapter='单选题'")
    cursor.execute("alter table questionbank auto_increment 1")
    for i in range(0, len(txt)):
        param = txt[i]
        sql = "insert into questionbank(book,chapter,question_type,question,selectA,selectB,selectC,selectD,isSelect) values('无线传感器网络','单选题','单选题',%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, param)
    # 提交到数据库执行
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()


def readWSN3():
    with open('WSN-多选题.txt', 'r', encoding='utf-8') as txt:
        txt = txt.readlines()
    for i, v in enumerate(txt):
        if txt[i].isspace():
            del txt[i]
        txt[i] = txt[i].replace('\n', '')
    txt = [txt[i:i + 6] for i in range(0, len(txt), 6)]
    for i in range(0, len(txt)):
        txt[i][-1] = txt[i][-1][-1]

    # 创建数据库连接
    conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="187139", db="mayuan")
    # 获取一个游标对象
    cursor = conn.cursor()
    # 设置参数i，for语句循环
    cursor.execute("delete from questionbank where book='无线传感器网络' and chapter='多选题'")
    cursor.execute("alter table questionbank auto_increment 1")
    for i in range(0, len(txt)):
        param = txt[i]
        sql = "insert into questionbank(book,chapter,question_type,question,selectA,selectB,selectC,selectD,isSelect) values('无线传感器网络','多选题','多选题',%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, param)
    # 提交到数据库执行
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()


readWSN3()
