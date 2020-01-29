import csv
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import telebot
import io
from telebot import types

bot = telebot.TeleBot('#')
print('started')

book_list = {}

dialog_key = False

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
            try:
                line = row.find('span', text=book_req)
                if line is not None:
                    book_name = re.sub(r'<.*?>', '', str(row))
                    file_name = re.findall(r'/b/\d+', str(row.find('a')))
                    info = get_book_info(file_name[0])
                    files[key] = [book_name, file_name, info]
                    key += 1
                else:
                    line = row.find('b', text=book_req)
                    if line is not None:
                        book_name = re.sub(r'<.*?>', '', str(row))
                        file_name = re.findall(r'/b/\d+', str(row.find('a')))
                        info = get_book_info(file_name[0])
                        files[key] = [book_name, file_name, info]
                        key += 1
            except:
                continue
    return files

def download(url, file_name):
    print(url) #download file from url to file
    urllib.request.urlretrieve('http://flibusta.is' + url + '/fb2', 'c:\\temp\\' + file_name +'.fb2') #TODO fix place to save

def get_book_info(url):
    soup = BeautifulSoup(get_html('http://flibusta.is' + url))
    info = soup.find('span', style="size").text
    return info

@bot.message_handler(commands=['start']) #if user send /help bot send back help
def start_message(message):
    global book_list, dialog_key
    book_list = {}
    dialog_key = False
    bot.send_message(message.chat.id, 'hello')

@bot.message_handler(commands=['help']) #if user send /help bot send back help
def make_keyboard(chatID, book_list):
    keyboard = types.InlineKeyboardMarkup()
    for key, book in book_list.items():
        #    bot.send_message(message.chat.id, (str(key) + ' ' + value[0] + ' ' + value[2]))
        callback_button = types.InlineKeyboardButton(text=str(book[0] + ' ' + book[2]), callback_data=str(key))
        keyboard.add(callback_button)
    bot.send_message(chatID, "Choose your destiny", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Загружаю!')
    try:
        selected = int(call.data)
        download(book_list[selected][1][0], book_list[selected][0])
        book = open(str('c:\\temp\\' + book_list[selected][0] +'.fb2'), 'rb')
        print(book)
        bot.send_document(call.message.chat.id, book)
        print('done')
    except:
        bot.send_message(call.message.chat.id, 'something wrong, try another file')


@bot.message_handler(content_types=['text']) #if user send text
def get_text_messages(message):
    print(message.text)
    main(message)
    #send_message(message, message.chat.id)

def main(message):
    global dialog_key, book_list
    #if dialog_key == False:
    book_list = {}
    book_req = message.text

    url = 'http://flibusta.is/booksearch?ask={}'.format('+'.join(urllib.parse.quote(book_req).split(' ')))
    book_req = book_req.split()[0].capitalize()
    #print(book_req)
    book_list = parse(get_html(url), book_req)
    if book_list == {}:
        print('wrong book name')
    for key, value in book_list.items():
        print(key, value[0], value[2])
    #for key, book in book_list: print(key,get_key book_list[book][0],  book_list[book][2] )
    #print(get_book_info('/b/21024'))
    #for key, value in book_list.items():
    #    bot.send_message(message.chat.id, (str(key) + ' ' + value[0] + ' ' + value[2]))
    dialog_key = True
    make_keyboard(message.chat.id, book_list)
    """else:
        
        try:
            selected = int(message.text)
            download(book_list[selected][1][0], book_list[selected][0])
            book = open(str('c:\\temp\\' + book_list[selected][0] +'.fb2'), 'rb')
            bot.send_document(message.chat.id, book)
            print('done')
            dialog_key = False
        except:
            bot.send_message(message.chat.id, 'try again')"""

    """selected = int(input("enter selected book\n"))
    #print(book_list[selected][1])
    try:
        download(book_list[selected][1][0], book_list[selected][0])
        print('done')
    except:
        print('oops!')"""

if __name__ == '__main__':
    bot.polling(none_stop = True)