import copy
import re

import pdfplumber


def read(num):
    with pdfplumber.open('马原题库.pdf') as pdf:
        first_page = pdf.pages[num]
        i = 0
        text1 = ''
        text2 = ''
        pattern1 = re.compile(r'[^A-E]')
        pattern2 = re.compile(r'[^1-9]')
        content = [0] * len(first_page.extract_words())
        while i < len(first_page.extract_words()):
            content[i] = first_page.extract_words()[i]['text']
            # print(content[i])
            i = i + 1
        i = 1
        count = 0
        # print(content)
        while i < len(content):
            if (content[i][len(content[i]) - 2] == ')') & (re.findall('[^()。 ]', content[i]) == []) | (
                    content[i][0] == ')') | (
                    re.findall(pattern1, content[i]) == []):
                content[i - 1] = content[i - 1] + content[i]
                count = count + 1
                for tag in range(i, (len(content) - 1)):
                    content[tag] = content[tag + 1]
            if not re.findall(pattern2, content[i]):
                content[i] = content[i] + content[i + 1]
                count = count + 1
                for tag in range(i + 1, (len(content) - 1)):
                    content[tag] = content[tag + 1]
            i = i + 1

        if count > 0:
            content[len(content) - 1] = ''
            i = len(content) - 2
            # print(content)
            while i > 0:
                if content[i] == content[i - 1]:
                    for tag in range(i, len(content)):
                        content[tag] = ''
                else:
                    break
                i = i - 1
            if len(content[i]) >= 2:
                if content[i][len(content[i]) - 2] == ')':
                    content[i] = ''
            if i > 0 & len(content[i]) > 0:
                if content[i][0] == ')':
                    content[i] = ''
            if not re.findall(pattern1, content[i]):
                content[i] = ''
        # print(content)
        i = 0
        while i < len(content):
            if content[i] != '':
                if i % 2 == 0:
                    text1 = text1 + content[i]
                else:
                    text2 = text2 + content[i]
            i = i + 1
        text = text1 + text2
        # print(text1)
        # print(text2)
        return text


def readall():
    with pdfplumber.open('马原题库.pdf') as pdf:
        lens = len(pdf.pages)
        text_all = ''
        for page in range(0, lens):
            text_all = text_all + read(page)
    with open('马原处理.txt', 'w', encoding='utf-8') as resultFile:
        resultFile.write(text_all)
