# -*- coding: cp1251 -*-
import sqlite3

class BAZA:

    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))
        
    def subscriber_actual(self,user_id):
        with self.connection:
            result = self.cursor.execute('SELECT `status` FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchone()
            return result[0]

    def add_subscriber(self, user_id, username, status = True):
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `name`, `status`) VALUES(?,?,?)", (user_id,username,status))

    def update_subscription(self, user_id, status):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
        self.connection.close()
