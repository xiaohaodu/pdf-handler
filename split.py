import copy
import re

from read import read


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
        split_1 = re.compile(r'([A-E]、|[0-9]+、|正确答案：[A-E×√]+(?!、))')
        split_3 = re.compile(r'([A-E]、|[0-9]+、)')
        res = re.split(split_1, texts)

        i = 0
        while i < len(res):
            if re.match(split_3, res[i]) is not None:
                res[i] = res[i] + res[i + 1]
                for tag in range(i + 1, (len(res) - 1)):
                    res[tag] = res[tag + 1]
            i = i + 1
        i = 0
        while i < len(res) - 1:
            if (res[i] == res[i + 1]) & (res[i] == res[len(res) - 2]) & (
                    res[i] == '))'):
                for tag in range(i, len(res)):
                    res[tag] = ''
            elif (res[i] == res[i + 1]) & (res[i] == res[len(res) - 2]):
                for tag in range(i + 1, len(res)):
                    res[tag] = ''
            i = i + 1
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
