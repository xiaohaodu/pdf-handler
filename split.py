import copy
import re
import pymysql


def split(chackname):
    with open(chackname, 'r', encoding='utf-8') as txt:
        texts = txt.read()
        all_list = []
        pattern1 = re.compile(r'[^A-E]')
        split_1 = re.compile(r'([A-E]、|[0-9]+、|正确答案：[A-E×√]+(?!、))')
        split_3 = re.compile(r'([A-E]、|[0-9]+、)')
        res = re.split(split_1, texts)

        i = 0
        count = 0
        while i < len(res):
            if re.match(split_3, res[i]) is not None:
                res[i] = res[i] + res[i + 1]
                count = count + 1
                for tag in range(i + 1, (len(res) - 1)):
                    res[tag] = res[tag + 1]
            i = i + 1
        if count > 0:
            res[len(res) - 1] = ''
            i = len(res) - 2
            # print(res)
            while i > 0:
                if res[i] == res[i - 1]:
                    for tag in range(i, len(res)):
                        res[tag] = ''
                else:
                    break
                i = i - 1
            if len(res[i]) > 2:
                if res[i][len(res[i]) - 2] == ')':
                    res[i] = ''
            if i > 0 & len(res[i]) > 0:
                if res[i][0] == ')':
                    res[i] = ''
            if not re.findall(pattern1, res[i]):
                res[i] = ''
        while None in res:  # 判断是否有空值在列表中
            res.remove(None)  # 如果有就直接通过remove删除
        while '' in res:  # 判断是否有空值在列表中
            res.remove('')  # 如果有就直接通过remove删除

        # print(res)
        chapter = ''
        is_chapter = re.compile(r'[0-9A-E正]+')
        i = 0
        my_list = []
        while i < len(res):
            if re.match(is_chapter, res[i][0]) is None:
                chapter = res[i]
                i = i + 1
                continue
            elif re.match('[0-9]+', res[i][0]) is not None:
                if len(my_list) != 0:
                    all_list.append(copy.deepcopy(my_list))
                    my_list.clear()
                my_list.append(chapter)
                my_list.append(res[i])
                i = i + 1
                continue
            my_list.append(res[i])
            i = i + 1
        # print(all_list)
        select = []
        true_false = []
        i = 0
        while i < len(all_list):
            if all_list[i][0][0] != '判':
                select.append(copy.deepcopy(all_list[i]))
            else:
                true_false.append(copy.deepcopy(all_list[i]))
            i = i + 1
        # print(select)

        i = 0
        while i < len(select):
            if len(select[i]) == 5:
                select[i].append(copy.deepcopy(select[i][4]))
                select[i][4] = ''
                select[i].append(copy.deepcopy(select[i][5]))
                select[i][5] = ''
                select[i].append(copy.deepcopy(select[i][6]))
                select[i][6] = ''
            i = i + 1

        i = 0
        while i < len(select):
            if len(select[i]) == 6:
                select[i].append(copy.deepcopy(select[i][5]))
                select[i][5] = ''
                select[i].append(copy.deepcopy(select[i][6]))
                select[i][6] = ''
            i = i + 1

        i = 0
        while i < len(select):
            if len(select[i]) == 7:
                select[i].append(copy.deepcopy(select[i][6]))
                select[i][6] = ''
            i = i + 1

        i = 0
        while i < len(select):
            if select[i][len(select[i]) - 1][len(select[i][len(select[i]) - 1]) - 1] == '：':
                select.remove(copy.deepcopy(select[i]))
            i = i + 1

        i = 0
        while i < len(select):
            if len(select[i]) != 8:
                select.remove(copy.deepcopy(select[i]))
            i = i + 1

        i = 0
        while i < len(select):
            select[i][7] = select[i][7].split('：')[1]
            i = i + 1

        i = 0
        while i < len(true_false):
            true_false[i][2] = true_false[i][2].split('：')[1]
            i = i + 1

        for index, v in enumerate(select):
            if len(v[-1]) > 1:
                select[index].insert(1, '多选')
            else:
                select[index].insert(1, '单选')
        # all_list[0].insert(1, '55')
        for index, v in enumerate(true_false):
            true_false[index].insert(1, '判断题')

        # 创建数据库连接
        conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="187139", db="mayuan")
        # 获取一个游标对象
        cursor = conn.cursor()
        # 设置参数i，for语句循环
        cursor.execute("delete from questionbank where book='马克思主义基本原理'")
        cursor.execute("alter table questionbank auto_increment 1")
        for i in range(0, len(select)):
            param = select[i]
            sql = "insert into questionbank(book,chapter,question_type,question,selectA,selectB,selectC,selectD,selectE,isSelect) values('马克思主义基本原理',%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, param)

        for i in range(0, len(true_false)):
            param = true_false[i]
            sql = "insert into questionbank(book,chapter,question_type,question,selectA,selectB,isSelect) values('马克思主义基本原理',%s,%s,%s,'√','×',%s)"
            cursor.execute(sql, param)
        # 提交到数据库执行
        conn.commit()
        # 关闭连接
        conn.close()
        cursor.close()
