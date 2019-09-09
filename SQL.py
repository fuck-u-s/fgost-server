# -*- coding: utf-8 -*-

import pymysql

class SQL:
    def __init__(self, ip="localhost", username="", pwd="", dbname="", charset='utf8'):
        self.ip = ip
        self.username = username
        self.pwd = pwd
        self.dbname = dbname
        self.charset = charset

    def db(self, cb):
        ret = False
        db = None
        cursor = None
        try:
            db = pymysql.connect(host=self.ip, port=3306, user=self.username, password=self.pwd, db=self.dbname, charset=self.charset)
            cursor = db.cursor()
            cb(cursor)
            ret = True
        except Exception as x:
            print("数据操作异常\t", x)
        finally:
            if cursor:
                cursor.close()
            if db:
                db.commit()
        return ret

    def query(self, sql, args=[]):
        ret = []
        db = None
        cursor = None
        try:
            db = pymysql.connect(host=self.ip, port=3306, user=self.username, password=self.pwd, db=self.dbname, charset=self.charset)
            cursor = db.cursor()
            cursor.execute(sql, args)
            ret = cursor.fetchall()
        except Exception as x:
            print("数据操作异常\t", x)
        finally:
            if cursor:
                cursor.close()
            if db:
                db.commit()
        return ret

    def update(self, sql, args):
        db = None
        cursor = None
        rowcount = 0
        try:
            db = pymysql.connect(host=self.ip, port=3306, user=self.username, password=self.pwd, db=self.dbname, charset=self.charset)
            cursor = db.cursor()
            rowcount = cursor.execute(sql, args)
        except Exception as x:
            print("数据操作异常\t", x)
        finally:
            if cursor:
                cursor.close()
            if db:
                db.commit()
        return rowcount

    def updates(self, sql, args):
        db = None
        cursor = None
        rowcount = 0
        try:
            db = pymysql.connect(host=self.ip, port=3306, user=self.username, password=self.pwd, db=self.dbname, charset=self.charset)
            cursor = db.cursor()
            rowcount = cursor.executemany(sql, args)
        except Exception as x:
            print("数据操作异常\t", x)
        finally:
            if cursor:
                cursor.close()
            if db:
                db.commit()
        return rowcount

# def dumps(obj):
#     return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)
# white_ips -p123456
if __name__ == '__main__':
    Sql = SQL("127.0.0.1", "root", "", "t_ips")
    rows = Sql.query("select * from t_hots")
    for row in rows:
        print(row)


