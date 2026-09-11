from telebot import *
import random
import os
from time import *

white_list = ['']

bot = telebot.TeleBot('вош токен')


@bot.message_handler(commands=['start'])
def start(message):
    global white_list
    if str(message.from_user.id) in white_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Выполнено')
        markup.add(btn1)
        bot.send_message(message.chat.id, 'бот запущен, напишите сообщение', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'упс, Вас нет в вайт листе, если Вы Ксюша обратитесь сюда @andre_plov', reply_markup=markup)



@bot.message_handler(func=lambda message: True)
def write_mes(message):
    global white_list
    if str(message.from_user.id) in white_list and message.text != 'Выполнено':
        bot.send_message(message.chat.id, 'записано')
        print(message.from_user.id)
        write_file(message.text, 'list.txt')
        update(message)
    elif str(message.text) == 'Выполнено':
        update(message)
        bot.send_message(message.chat.id, 'Выберите пункт и он бует отмечен значком {✅}')
        bot.register_next_step_handler(message, what_number)


def write_file(message, file_name):
    with open(file_name, 'a', encoding='utf-8') as file:
        file.seek(0, 2)
        file.write('\n')
        file.write(f'{message}^')




def update(message): # вывод итогового сообщения с планами
    bot.send_message(message.chat.id, read_file('list.txt', 'for_message'))


def read_file(name, flag):
    with open(name, 'r', encoding='utf-8') as file:
        file.seek(0, 0)
        file_logs = file.readlines()
    while '\n' in file_logs: # удаление лишних \n
        try:
            file_logs_remove = file_logs.remove('\n')
        except ValueError:
            break
    if flag == 'for_message':
        num = 0
        text = ''
        for i in file_logs:
            num += 1
            text += f'{str(num)}. {i}'
        return text.replace('^', '')
    else:
        num = 0
        text = ''
        for i in file_logs:
            num += 1
            text += f'{i}'
        return text


def what_number(message):
    try:
        replace_nth('^', int(message.text), '#')
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный тип данных, попроьуйте снова')
        bot.register_next_step_handler(message, what_number)


def replace_nth(char, n, replacement):
    with open('list.txt', 'r', encoding='utf-8') as file:
         s = file.readlines()
    count = 0
    for i, c in enumerate(s):
        if c == char:
            count += 1
            if count == n:
                print(s[:i] + replacement + s[i+1:])
                return s[:i] + replacement + s[i+1:]
    print(s)
    return s


    # with open('list.txt', 'w', encoding='utf-8') as file:
    #     file.write(logs_rep)




if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)