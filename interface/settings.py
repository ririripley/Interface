# -*- coding: utf-8 -*-

import os
import sys

from interface import app
#在Python中，每一个有效的Python文件（.py）都是模块。每一个包
#含__init__.py文件的文件夹都被视作包，包让你可以使用文件夹来组织
#模块。__init__.py文件通常被称作构造文件，文件可以为空，也可以用
#来放置包的初始化代码。当包或包内的模块被导入时，构造文件将被自
#动执行。

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
#，由于配置文件
#被放到了程序包内，为了定位到位于项目根目录的数据库文件，使用
#os.path.dirname（app.root_path）获取上层目录,app.root_path属性存储
#程序实例所在的路径

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)

#数据库URL和密钥都会首先从环境变量获取。

MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = ('Group Project', MAIL_USERNAME)

MAIL_SUBJECT_PREFIX = '[JMT]'
