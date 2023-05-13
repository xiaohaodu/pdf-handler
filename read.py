import copy
import re
import pdfplumber


def read(filename, num):
    with pdfplumber.open(filename) as pdf:
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


def readall(readname,outputname):
    with pdfplumber.open(readname) as pdf:
        lens = len(pdf.pages)
        content_all = []
        for page in range(0, lens):
            content_all.append(copy.deepcopy(read(readname,page)))
            content_all.append(copy.deepcopy("  "))
    text1 = ''
    text2 = ''
    pattern1 = re.compile(r'[^A-E]')
    pattern2 = re.compile(r'[^1-9]')
    i = 1
    while i < len(content_all):
        if (content_all[i][len(content_all[i]) - 2] == ')') & (re.findall('[0-9]+、', content_all[i]) == []) | (
                content_all[i][0] == ')') | (
                re.findall(pattern1, content_all[i]) == []):
            content_all[i - 1] = content_all[i - 1] + content_all[i]
            for tag in range(i, (len(content_all) - 1)):
                content_all[tag] = content_all[tag + 1]
        if not re.findall(pattern2, content_all[i]):
            content_all[i] = content_all[i] + content_all[i + 1]
            for tag in range(i + 1, (len(content_all) - 1)):
                content_all[tag] = content_all[tag + 1]
        i = i + 1
    i = len(content_all) - 1
    while i > 0:
        if (content_all[i] == content_all[i - 1]) & (re.findall('[^()。 ]', content_all[i]) == []) | (
                content_all[len(content_all) - 1] == ')'):
            for tag in range(i, len(content_all)):
                content_all[tag] = ''
        elif (content_all[i] == content_all[i - 1]) & (re.findall('[^()。 ]', content_all[i]) == []):
            for tag in range(i, len(content_all)):
                content_all[tag] = ''
        i = i - 1
    i = 0
    while i < len(content_all):
        if content_all[i] != '':
            if i % 2 == 0:
                text1 = text1 + content_all[i]
            else:
                text2 = text2 + content_all[i]
        i = i + 1
    text = text1 + text2
    with open(outputname, 'w', encoding='utf-8') as resultFile:
        resultFile.write(text)
