import telebot
import config
import sqlite3

class BAZA:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()
        
    def searchData(self):
       self.cursor.execute("SELECT user_id,name FROM 'subscriptions'")
       rows = self.cursor.fetchall()
       data_list = [row for row in rows]
       return data_list
   
    def search_id(self,id):
         self.cursor.execute("SELECT user_id FROM 'subscriptions' WHERE id=?", (id,))
         row = self.cursor.fetchone()
         return row[0] if row else None
    
    def close(self):
        self.connection.close()
        
baza = BAZA("data.db")

bot = telebot.TeleBot(config.token)

a=1
for i in baza.searchData():
    print(i, a)
    a+=1
    
while True:
    Var = input("Какому пользователю?\n")
    try:
        user_id = baza.search_id(int(Var))
        print(f"Выбран: {user_id}")
        break
    except:
        print("Ошибка!")
        
while True:
    try:
        message = input("Что отправить?\n")
        bot.send_message(user_id, message)
        break
    except:
        print("Ошибка!")
