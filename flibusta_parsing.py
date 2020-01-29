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
    key = 0
    soup = BeautifulSoup(html)
    rows = soup.findAll('li')
    
    for row in rows:
        if str(row).find('sequence') == -1:
            #print(row)
            #print(str(row) + '\n')
            line = row.find('span', text=book_req)
            if line is not None: #TODO check 'sequence' tag
                book_name = re.sub(r'<.*?>', '', str(row))
                file_name = re.findall(r'/b/\d+', str(row.find('a')))
                info = get_book_info(file_name[0])
                files[key] = [book_name, file_name, get_book_info(file_name[0])]
                key += 1
                #print(book_name, file_name, info)
            else:
                line = row.find('b', text=book_req)
                if line is not None:
                    book_name = re.sub(r'<.*?>', '', str(row))
                    file_name = re.findall(r'/b/\d+', str(row.find('a')))
                    info = get_book_info(file_name[0])
                    files[key] = [book_name, file_name, get_book_info(file_name[0])]
                    key += 1
                    #print(book_name, file_name, info)
    #print(files)
    return files

def download(url, file_name): #download file from url to file
    urllib.request.urlretrieve('http://flibusta.is' + url + '/fb2', 'c:\\temp\\' + file_name +'.fb2') #TODO fix place to save

def get_book_info(url):
    soup = BeautifulSoup(get_html('http://flibusta.is' + url))
    info = soup.find('span', style="size").text
    return info

def main():
    while True:
        book_req = input("enter book name\n")
        url = 'http://flibusta.is/booksearch?ask={}'.format('+'.join(urllib.parse.quote(book_req).split(' ')))
        book_req = book_req.split()[0].capitalize()
        #print(book_req)
        book_list = parse(get_html(url), book_req)
        if book_list == {}:
            print('wrong book name')
            continue
        for key, value in book_list.items():
            print(key, value[0], value[2])
        #for key, book in book_list: print(key,get_key book_list[book][0],  book_list[book][2] )
        #print(get_book_info('/b/21024'))
        selected = int(input("enter selected book\n"))
        #print(book_list[selected][1])
        try:
            download(book_list[selected][1][0], book_list[selected][0])
            print('done')
        except:
            print('oops!')

if __name__ == '__main__':
    main()