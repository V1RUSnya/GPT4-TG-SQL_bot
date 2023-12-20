import g4f
import telebot
from time import sleep
from g4f.Provider import Bing
import sqlite3
from database import BAZA
import config

g4f.debug.logging = True # enable logging
g4f.check_version = False
# print(g4f.version)

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
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот с настоящей нейросетью gpt-4!\nЗадавайте любые вопросы!".format(message.from_user, bot.get_me()), parse_mode='html')
    

@bot.message_handler(commands=['subscribe'])
def subs(message):
    if (not baza.subscriber_exists(message.from_user.id)):
        baza.add_subscriber(message.from_user.id, message.from_user.first_name)
        bot.send_message(message.chat.id, "Вы успешно подписались!")
        
    elif (baza.subscriber_exists(message.from_user.id) and not baza.subscriber_actual(message.from_user.id)):
        baza.update_subscription(message.from_user.id, True)
        bot.send_message(message.chat.id, "Вы снова подписаны!")
    else:
        baza.update_subscription(message.from_user.id, True)
        bot.send_message(message.chat.id, "Вы уже подписались!")
        
@bot.message_handler(commands=['unsubscribe'])
def unsubs(message):
    if (baza.subscriber_exists(message.from_user.id) and baza.subscriber_actual(message.from_user.id)):
        baza.update_subscription(message.from_user.id, False)
        bot.send_message(message.chat.id, "Вы успешно отписались!")
    else:
        bot.send_message(message.chat.id, "Вы не подписаны!")
    
@bot.message_handler(content_types=['text'])
def ask(message):
    ps = ""
    textCloud = ""
    limit = 0
    if (subs_check(message.from_user.id)):
        try:
            print("\n\nВопрос: {0}, от пользователя {1.first_name}\n".format(message.text, message.from_user))
            response = g4f.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": ps + message.text}],
                proxy="http://216.80.39.89:3129",
                provider= Bing,
                stream=True,
            )
            sent_message = bot.send_message(message.chat.id, "...")
            for messaga in response:
                print(messaga, flush=True, end='')
                textCloud += messaga
                limit+=1
                if limit == 15:
                    limit = 0
                    try:
                        bot.edit_message_text(textCloud, message.chat.id, sent_message.message_id)
                    except RuntimeError as e: 
                        print(f"\n\nПопытка восстановления\nОшибка: {e}\n\n")
                        sleep(5)
                    mem = textCloud
            if textCloud != mem:        
                bot.edit_message_text(textCloud, message.chat.id, sent_message.message_id) 
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Ошибка: {e}! Ожидание 5 секунд")
            sleep(5)
        except AttributeError as e:
            print(f"Ошибка: {e}!")
    else:
        bot.send_message(message.chat.id, "Пожалуйста зарегистрируйтесь! /subscribe")

while True:
    try:        
        bot.polling(none_stop=True)
    except RuntimeError:
        print(f"\n\n\nПроизошла ошибка.\n\n"*2)
        sleep(60)