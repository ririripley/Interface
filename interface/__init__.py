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
    from interface.models import User
    return User.query.get(int(user_id))

login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 're_authenticate'
# login_manager.needs_refresh_message = 'Your custom message'
login_manager.needs_refresh_message_category = 'warning'
'''
current_user是当前用户的代理对象，我们经常借助它来调用User类的方
法和属性，但是当用户未登录时，current_user指向的用户对象是FlaskLogin提供的匿名用户类，而这个类并没有can（）方法可供调用
'''
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


'''
你在这里也许会疑惑，既然有了程序实例app对象，为什么还需要
current_app变量。在不同的视图函数中，request对象都表示和视图函数
对应的请求，也就是当前请求（current request）。而程序也会有多个程
序实例的情况，为了能获取对应的程序实例，而不是固定的某一个程序
实例，我们就需要使用current_app变量，
Flask会自动帮我们激活程序上下文：
·当我们使用flask run命令启动程序时
·执行使用@app.cli.command（）装饰器注册的flask命令时。


当请求进入时，Flask会自动激活请求上下文，这时我们可以使用
request和session变量。。另外，当请求上下文被激活时，程序上下文也被
自动激活。当请求处理完毕后，请求上下文和程序上下文也会自动销
毁。也就是说，在请求处理时这两者拥有相同的生命周期。

如果你需要在没有激活上下文的情况下使用这些变量，可以手动激
活上下文。程序上下文对象使用app.app_context（）获取，我们可以使用with
语句执行上下文操作
或是显式地使用push（）方法推送（激活）上下文，在执行完相关
操作时使用pop（）方法销毁上下文：
而请求上下文可以通过test_request_context（）方法临时创建：

current_app变量只有在程序上下文被激活后
才可以使用


'''