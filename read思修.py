import pdfplumber


def read(filename, num):
    with pdfplumber.open(filename) as pdf:
        page = pdf.pages[num]
        content = ''
        for char in page.chars:
            content += char['text']
        return content


def readpage(page):
    content = ''
    for char in page.chars:
        content += char['text']
    return content


def readall(filename, outputname):
    with pdfplumber.open(filename) as pdf:
        contentall = ''
        for page in pdf.pages:
            contentall += readpage(page)
    with open(outputname, 'w', encoding='utf-8') as resultFile:
        resultFile.write(contentall)
