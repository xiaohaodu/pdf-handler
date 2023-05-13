import copy
import re
import pymysql


def split(split_name):
    with open(split_name, 'r', encoding='utf-8') as txt:
        texts = txt.read().replace("\xa0", "")
        split_reg = re.compile(
            r'([（(][A-Z]+[）)]|[A-Z]|[一二三四五六七八九十]、|[0-9]+[．.、]|(?:绪论|第[一二三四五六七八九十]章)[^一二三四五六七八九十A-Z0-9]*)')
        split2 = re.compile(r'([A-Z]|[一二三四五六七八九十]、|[0-9]+[．.、])')
        split3 = re.compile(r'([（(][A-Z]+[）)])')
        split4 = re.compile(r'([A-Z])')
        texts = re.split(split_reg, texts)
        for index in range(len(texts) - 1, -1, -1):
            if texts[index] == '。' or texts[index] == '':
                del texts[index]
            elif re.match(split2, texts[index]):
                texts[index] += texts[index + 1]
                del texts[index + 1]
        for index in range(len(texts) - 1, -1, -1):
            if re.match(split3, texts[index]) and re.match(split4, texts[index + 1]) is None:
                texts[index] += texts[index + 1]
                del texts[index + 1]
        for index in range(len(texts) - 1, -1, -1):
            if re.match(split4, texts[index - 1]) is None and re.match(split3, texts[index]):
                texts[index - 1] += texts[index]
                del texts[index]

        split5 = re.compile(r'((?:绪论|第[一二三四五六七八九十]章)[^一二三四五六七八九十A-Z0-9]*)')
        split6 = re.compile(r'([一二三四五六七八九十]、[^一二三四五六七八九十A-Z0-9]*)')
        split7 = re.compile(r'([0-9]+[．.、])')
        split8 = re.compile(r'([A-Z])')
        chapter = ''
        question_types = ''
        list = []
        all_list = []
        for index, value in enumerate(texts):
            chapter_temp = re.match(split5, value)
            chapter = chapter_temp.group() if chapter_temp else chapter
            question_types_temp = re.match(split6, value)
            question_types = question_types_temp.group() if question_types_temp else question_types
            if re.match(split7, value):
                all_list.append(copy.deepcopy(list))
                list.clear()
                list.append(chapter)
                list.append(question_types)
                list.append(value)
            elif re.match(split8, value):
                list.append(value)
        del all_list[0]
        split9 = re.compile(r'([A-Z]+)')
        for index, v in enumerate(all_list):
            is_select = re.search(split9, all_list[index][2]).group()
            all_list[index][2] = re.sub(split9, '', all_list[index][2])
            all_list[index].append(is_select)

        for index, v in enumerate(all_list):
            if len(all_list[index]) == 8:
                all_list[index].insert(-1, '')
            elif len(all_list[index]) == 7:
                all_list[index].insert(-1, '')
                all_list[index].insert(-1, '')

        # 查看是否完成余位补充
        # for index, v in enumerate(all_list):
        #     if len(v) != 9:
        #         print(v)
        # print(all_list)

        # 创建数据库连接
        conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="187139", db="mayuan")
        # 获取一个游标对象
        cursor = conn.cursor()
        # 设置参数i，for语句循环
        cursor.execute("delete from questionbank where book='思想道德基础与法律修养'")
        cursor.execute("alter table questionbank auto_increment 1")
        for i in range(0, len(all_list)):
            param = all_list[i]
            sql = "insert into questionbank(book,chapter,question_type,question,selectA,selectB,selectC,selectD,selectE,isSelect) values('思想道德基础与法律修养',%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, param)
        # 提交到数据库执行
        conn.commit()
        # 关闭连接
        cursor.close()
        conn.close()
