# -*- coding: cp1251 -*-
import g4f
import telebot
from time import sleep
from g4f.Provider import Yqcloud
import sqlite3
from database import BAZA
import config

g4f.debug.logging = True # enable logging
g4f.check_version = False
print(g4f.version)

bot = telebot.TeleBot(config.token)

baza = BAZA("data.db")

def subs_check(messageID):
    if (baza.subscriber_exists(messageID) and baza.subscriber_actual(messageID)):
        A = True
    else:
        A = False
    return A    

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "����� ����������, {0.first_name}!\n� - <b>{1.first_name}</b>, ��� � ���������� gpt-4!\n��������� ����� �������!".format(message.from_user, bot.get_me()), parse_mode='html')
    

@bot.message_handler(commands=['subscribe'])
def subs(message):
    if (not baza.subscriber_exists(message.from_user.id)):
        baza.add_subscriber(message.from_user.id, message.from_user.first_name)
        bot.send_message(message.chat.id, "�� ������� �����������!")
        
    elif (baza.subscriber_exists(message.from_user.id) and baza.subscriber_actual(message.from_user.id)):
        baza.update_subscription(message.from_user.id, True)
        bot.send_message(message.chat.id, "�� ����� ���������!")
    else:
        baza.update_subscription(message.from_user.id, True)
        bot.send_message(message.chat.id, "�� ��� �����������!")
        
@bot.message_handler(commands=['unsubscribe'])
def subs(message):
    if (baza.subscriber_exists(message.from_user.id) and baza.subscriber_actual(message.from_user.id)):
        baza.update_subscription(message.from_user.id, False)
        bot.send_message(message.chat.id, "�� ������� ����������!")
    else:
        bot.send_message(message.chat.id, "�� �� ���������!")
    
@bot.message_handler(content_types=['text'])
def ask(message):
    ps = "(����������: ������� �� ������� �����) "
    if (subs_check(message.from_user.id)):
        try:
            print("\n\n������: {0}, �� ������������ {1.first_name}\n".format(message.text, message.from_user))
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": ps + message.text}],
                provider= Yqcloud,
                stream=True,
            )
            textCloud = ""
            limit = 0
            sent_message = bot.send_message(message.chat.id, "...") 
            for messaga in response:
                print(messaga, flush=True, end='')
                textCloud += messaga
                limit+=1
                if limit == 3:
                    limit = 0
                    bot.edit_message_text(textCloud, message.chat.id, sent_message.message_id)
                    mem = textCloud
            if textCloud != mem:        
                bot.edit_message_text(textCloud, message.chat.id, sent_message.message_id) 
        except telebot.apihelper.ApiTelegramException as e:
            print(f"������: {e}! �������� 5 ������")
            sleep(5)
    else:
        bot.send_message(message.chat.id, "���������� �����������������! /subscribe")
        
bot.polling(none_stop=True)