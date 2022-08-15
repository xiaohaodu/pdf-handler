import copy
import re

import pdfplumber

from read import read


def read_1(num):
    with pdfplumber.open('马原题库.pdf') as pdf:
        first_page = pdf.pages[num]
        i = 0
        content = [0] * len(first_page.extract_words())
        while i < len(first_page.extract_words()):
            content[i] = first_page.extract_words()[i]['text']
            # print(content[i])
            i = i + 1
    return content


def readall_1():
    with pdfplumber.open('马原题库.pdf') as pdf:
        lens = len(pdf.pages)
        content_all = []
        for page in range(0, lens):
            content_all.append(copy.deepcopy(read(page)))
            content_all.append(copy.deepcopy("  "))
    text1 = ''
    text2 = ''
    pattern1 = re.compile(r'[^A-E]')
    pattern2 = re.compile(r'[^1-9]')
    i = 1
    while i < len(content_all):
        if (content_all[i][len(content_all[i]) - 2] == ')') | (content_all[i][0] == ')') | (
                re.findall(pattern1, content_all[i]) == []):
            content_all[i - 1] = content_all[i - 1] + content_all[i]
            for tag in range(i, (len(content_all) - 1)):
                content_all[tag] = content_all[tag + 1]
        if not re.findall(pattern2, content_all[i]):
            content_all[i] = content_all[i] + content_all[i + 1]
            for tag in range(i + 1, (len(content_all) - 1)):
                content_all[tag] = content_all[tag + 1]
        i = i + 1
    i = 0
    while i < len(content_all) - 1:
        if (content_all[i] == content_all[i + 1]) & (content_all[i] == content_all[len(content_all) - 2]) & (content_all[i] == '))'):
            for tag in range(i, len(content_all)):
                content_all[tag] = ''
        elif (content_all[i] == content_all[i + 1]) & (content_all[i] == content_all[len(content_all) - 2]):
            for tag in range(i + 1, len(content_all)):
                content_all[tag] = ''
        i = i + 1
    i = 0
    while i < len(content_all):
        if content_all[i] != '':
            if i % 2 == 0:
                text1 = text1 + content_all[i]
            else:
                text2 = text2 + content_all[i]
        i = i + 1
    text = text1 + text2
    with open('马原处理.txt', 'w', encoding='utf-8') as resultFile:
        resultFile.write(text)
