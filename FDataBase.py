import sqlite3
import time
import math
 
class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
 


    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            dict = [{k: item[k] for k in item.keys()} for item in res] # change output sqlRow->dict
            if res: return dict
        except:
            print("Reading db error")
        return []



    def addUser(self, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("User with this email exists")
                return False
 
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Db error "+str(e))
            return False
 
        return True   



# for login
    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User is not found")
                return False 
 
            return res
        except sqlite3.Error as e:
            print("Db error "+str(e))
 
        return False



    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = {email} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User is not found")
                return False 
 
            return res
        except sqlite3.Error as e:
            print("Db error "+str(e))
 
        return False

    def getQoutes(self):
        sql = '''SELECT * FROM qoutes'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            dict = [{k: item[k] for k in item.keys()} for item in res]
            list_qoutes= [[line[keys] for keys in line] for line in dict]

            if res: return list_qoutes
        except:
            print("Reading db error")
        return []