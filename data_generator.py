from bs4 import BeautifulSoup
import requests
import pandas as pd
import glob
import string
import os
import codecs

BASE_BOOK_URL = 'https://www.gutenberg.org/browse/scores/top'

html = requests.get(BASE_BOOK_URL).text
soup = BeautifulSoup(html)

unq_code = {}
for s in soup.findAll('li'):
    url = s.a['href']
    if 'ebooks' in url:
        book_code = url.split('/')[-1]
        if book_code != '' and book_code != "offline_catalogs.html":
            unq_code[int(book_code)] = s.a.text
        
BOOK_TXT_BASE = 'https://www.gutenberg.org/files/'
book_urls = []
for code in unq_code:
    book_urls.append(os.path.join(BOOK_TXT_BASE, f'{code}/{code}-0.txt'))

for b in book_urls:
    name = b.split('/')[-2]
    html = requests.get(b).text
    with codecs.open(f'data/books/{name}.txt', 'w', 'utf-8') as infile:
        infile.write(html)
        

BASE_GLOSS_URL = 'https://www.gradesaver.com/'
TERMINAL = '/study-guide/glossary-of-terms'

def punctuations(data_str):
    data_str = data_str.replace("'s", "")
    for x in data_str.lower():
        if x in string.punctuation: 
            data_str = data_str.replace(x, "")
    return data_str

for book in glob.glob('data/books/*'):
    code = book.split('/')[-1].split('.')[0]
    try:
        bookname = unq_code[int(code)]
        bookname = bookname.split(' by ')[0].lower()
        bookname = punctuations(bookname)
        bookname = bookname.replace(" ", "-")
        html = requests.get(BASE_GLOSS_URL+bookname+TERMINAL).text
        soup = BeautifulSoup(html)
        tt = []
        for term in soup.findAll("section", {"class": "linkTarget"}):
            tt.append([term.h2.text.lower().strip(), term.p.text.lower().strip()])
        if len(tt):
            print (f'Done: {bookname}')
            data = pd.DataFrame(tt, columns=['word', 'def'])
            data.to_csv(f'data/ground_truth/{code}.csv', sep='\t', encoding='utf-8', index=False)
        else:
            print (f'Skipped: {bookname}')
    except Exception as e: print (e)

