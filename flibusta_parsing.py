import csv
import urllib.request
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error


def get_html(url): #get html file from url
    response = urllib.request.urlopen(url)
    return response.read()

def parse(html, book_req=''): #parsing html to find book name and url
    files = {}
    soup = BeautifulSoup(html)
    rows = soup.findAll('li')

    for row in rows:
        #print(str(row) + '\n')
        cols = row.find('span', text=book_req)
        if cols is not None:
            book_name = re.sub(r'<.*?>', '', str(row))
            file_name = re.findall(r'/b/\d+', str(row.find('a')))
            files[book_name] = file_name
            print(book_name, get_book_info(file_name[0]))
        else:
            cols = row.find('b', text=book_req)
            if cols is not None:
                book_name = re.sub(r'<.*?>', '', str(row))
                file_name = re.findall(r'/b/\d+', str(row.find('a')))
                files[book_name] = file_name
                print(book_name, get_book_info(file_name[0]))

    return files

def download(url, file_name): #download file from url to file
    urllib.request.urlretrieve('http://flibusta.is' + url + '/fb2', 'c:\\temp\\file.fb2') #TOFO fix place to save

def get_book_info(url):
    soup = BeautifulSoup(get_html('http://flibusta.is' + url))
    info = soup.find('span', style="size").text
    return info

def main():
    book_req = input()
    url = 'http://flibusta.is/booksearch?ask={}'.format('+'.join(urllib.parse.quote(book_req).split(' ')))
    book_req = book_req.split()[0].capitalize()
    print(book_req)
    book_list = parse(get_html(url), book_req)
    for book in book_list: print(book) 
    
    #print(get_book_info('/b/21024'))

if __name__ == '__main__':
    main()