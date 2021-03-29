import os
from flask import Flask, send_file, send_from_directory
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from updatafolder import GetUploadFile
from pathlib import Path

app = Flask(__name__)  # 实例化flask app


LOCAL_FOLDER = r'E:\svn\游戏申测_游戏二组'


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:pokercity@172.19.65.74:3306/demo?charset=utf8'
    run_times = {
        'day_of_week': 'mon-sun',   # 配置一周哪几天执行
        'hour': 10,                 # 配置执行的准确时间，小时
        'minute': 10,               # 配置执行的准确时间，分钟
        'second': 0,                # 配置执行的准确时间，秒
        'misfire_grace_time': 360   # 配置任务便宜时间阈值，秒
    }
    JOBS = [
        {
            'id': 'updata_project_data',  # 一个标识
            'func': '__main__:update_project',  # 指定运行的函数
            # 'args': (1, 2),  # 传入函数的参数
            'trigger': 'interval',  # 指定 定时任务的类型
            # 'day_of_week': run_times.get('day_of_week'),
            # day_of_week (int|str) – 周内第几天或者星期几 (范围0-6 或者 mon,tue,wed,thu,fri,sat,sun)
            'seconds': 60,  # 运行的间隔时间
            # 'hour': run_times.get('hour'),  # hour (int|str) – 时 (范围0-23)
            # 'minute': run_times.get('minute'),  # minute (int|str) – 分 (范围0-59)
            # 'second': run_times.get('second'),  # second (int|str) – 秒 (范围0-59)
            'misfire_grace_time': run_times.get('misfire_grace_time')  # 任务不能准时进行的阈值
        }
    ]

    SCHEDULER_API_ENABLED = True
    # 设置sqlalchemy自动跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

def update_project():
    print("更新了一次文件信息~~~~~~")
    GetUploadFile.updateproject(db)


if __name__ == '__main__':
    app = Flask(__name__)  # 实例化flask
    app.config.from_object(Config())  # 为实例化的 flask 引入配置
    db = SQLAlchemy(app)
    scheduler = APScheduler()  # 实例化 APScheduler
    scheduler.init_app(app)  # 把任务列表放入 flask
    scheduler.start()  # 启动任务列表
    app.run(debug=True, port=9044, host='0.0.0.0')