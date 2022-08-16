import copy
import re

import pymysql

from read import read
from read_1 import read_1


def split():
    with open('马原处理.txt', 'r', encoding='utf-8') as txt:
        texts = txt.read()
        i = 0
        all_list = []
        split_1 = re.compile(
            r'(正确答案：[A-E]+(?!、)|正确答案：[√×]|[0-9]+[^A-E正√×]+|[A-E]、[^0-9A-E正]*[0-9]*[万]*元[^0-9A-E正]*[^0-9A-E正]*[0-9]*[万]*元[^0-9A-E正]*|[A-E]、[^0-9A-E正]*[0-9]*[万]*元[^0-9A-E正]*|[A-E]、[^0-9A-E正]*[0-9]{4}[^0-9A-E正]+|[A-E]、[^0-9A-E正]*[0-9]{2}年代[^0-9A-E正]+|[A-E]、[^0-9A-E正]+)')
        res = re.split(split_1, texts)

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
        print(all_list)


def split_2():
    with open('马原处理.txt', 'r', encoding='utf-8') as txt:
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
            if len(select[i]) == 7:
                select[i].append(copy.deepcopy(select[i][6]))
                select[i][6] = ''
            i = i + 1

        i = 0
        while i<len(select):
            if len(select[i]) > 8:
                print(select[i])
            i = i + 1

        # print(select)
        # print(read(0))

        # print(true_false)
        # # 创建数据库连接
        # conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="187139", db="mayuan")
        # # 获取一个游标对象
        # cursor = conn.cursor()
        # # 设置参数i，for语句循环
        # for i in range(1, len(all_list)):
        #     param = str(i)
        #     sql = "insert into questionbank(chapter,question,selectA,selectB,selectC,selectD,selectE,isSelect,true_or_false,) values(%s,%s,%s)"
        #     cursor.execute(sql, param)
        #     conn.commit()
        # # 关闭连接
        # conn.close()
        # cursor.close()
