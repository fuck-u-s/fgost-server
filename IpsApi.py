# -*- coding: utf-8 -*-

import json
import time

from flask import Flask
from gevent.pywsgi import WSGIServer

from mysql.SQL import SQL

Sql = SQL("192.168.8.105", "root", "IGszGpeWQ!al!Wu^", "ips")

app = Flask(__name__)

nodes = dict()


@app.route("/index.html")
def ws():
    return "hello"


@app.route("/api/oninfos/<serial>")  # 参数为用户名
def index(serial):
    if serial and len(serial) > 0:
        count = Sql.update("UPDATE t_ips set last_time=UNIX_TIMESTAMP() WHERE serial=%s", [serial])
        print(serial)
        if count > 0:
            print("index", serial, time.time())
            return "ok"
    print("index2", serial, time.time())
    return "fail"


@app.route("/api/onswitch/<serial>/start")  # 提交切换ip请求
def onSwitchStart(serial):
    if serial and len(serial) > 0:
        nodes[serial] = 1
        print("onSwitchStart", serial, time.time())
        return "ok"
    print("onSwitchStart2", serial, time.time())
    return "fail"


@app.route("/api/onswitch/<serial>/end")  # 判断切换ip请求
def onSwitchEnd(serial):
    if serial and len(serial) > 0 and nodes.__contains__(serial):
        del nodes[serial]
        print("onSwitchEnd", serial, time.time())
        return "ok"
    print("onSwitchEnd2", serial, time.time())
    return "fail"


@app.route("/api/onboot/<serial>")  # 参数为用户名
def onboot(serial):
    print(serial)
    if serial and len(serial) > 0:
        keys = ["server_port", "serial", "protocol", "user", "passwd", "dns", "token", "last_time"]
        selectKeys = ",".join(keys)
        data = Sql.query(" ".join(["SELECT", selectKeys, "from t_ips WHERE serial=%s"]), [serial])
        if len(data) > 0:
            result = dict()
            i = 0
            for key in keys:
                result[key] = data[0][i]
                i += 1
            print("onboot", serial, time.time())
            return json.dumps(result)
    print("onboot2", serial, time.time())
    return ""


@app.errorhandler(404)
def errorHandler(e):
    print(e)
    return "hello"


def bootService(port):
    # 创建一个WebSocket服务器
    http_serv = WSGIServer(("0.0.0.0", port), app)
    # 开始监听HTTP请求
    http_serv.serve_forever()


if __name__ == '__main__':
    print("boot server")
    bootService(80)
