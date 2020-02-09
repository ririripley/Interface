# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager, AnonymousUserMixin



'''
从构造文件中导入变量时不需要注明构造文件的路径，只需要从包
名称导入，比如导入在构造文件中定义的程序实例app可以使用
from interface import app
'''

app = Flask('interface')
app.config.from_pyfile('settings.py') #在创建程序实例后，使用config对象的from_pyfile（）方法即可加
#载配置，传入配置模块的文件名作为参数
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

login_manager = LoginManager() #Flask-Login uses sessions for authentication.
db = SQLAlchemy(app)
mail = Mail(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 'auth.re_authenticate'
# login_manager.needs_refresh_message = 'Your custom message'
login_manager.needs_refresh_message_category = 'warning'

from interface import views, errors, commands

'''
当我们启动程序时，首先被执行的是包含程序实例的脚本，即构造
文件。但注册在程序实例上的各种处理程序均存放在其他脚本中，比如
视图函数存放在views.py中、错误处理函数则存放在errors.py中。如果不
被执行，那么这些视图函数和错误处理函数就不会注册到程序上，那么
程序也无法正常运行。为了让使用程序实例app注册的视图函数，错误
处理函数，自定义命令函数等和程序实例关联起来，我们需要在构造文
件中导入这些模块。因为这些模块也需要从构造文件中导入程序实例，
所以为了避免循环依赖，这些导入语句在构造文件的末尾定义。
'''