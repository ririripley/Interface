# -*- coding: utf-8 -*-
"""
    :author: Ripley
"""
import unittest

from flask import abort

from interface import app, db
from interface.models import Message, User, Mathmodel
from interface.commands import initdb
from flask import jsonify
import json
from flask import url_for


class InterfaceTestCase(unittest.TestCase):

    # def setUp(self):
    #     app = create_app('testing')
    #
    # self.context = app.test_request_context()  # 创建上下文对象
    # self.context.push()  # 推送上下文
    # self.client = app.test_client()
    # db.create_all()
    #



    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        db.create_all() #使用db.create_all（）方法创建数据库和表。
        self.client = app.test_client()#创建测试客户端对象, 将其保存为类属性self.client，
        self.runner = app.test_cli_runner() #Flask提供了app.test_cli_runner（）方法用于在测试中调用命令函数、捕捉输出


        user = User(username='hzj', email='hzj.com')
        user.set_password('123')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        #测试时我们需要手动调用db.session.remove（）以清除会话，最后调用db.drop_all（）清除数据库。


    def test_app_exist(self):
        self.assertFalse(app is None)
        #测试程序实例是否存在

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])
        #测试程序配置键TESTING是否为True
    #
    # def test_sendQUE(self, username = "test"):
    #     with app.app_context():
    #         response = self.client.post('/postQUE',
    #                                     data=json.dumps(dict(username='hzj')),
    #                                     content_type='application/json')
    #         data = response.get_json()
    #         print(data)

    # User Function.test
    def test_success_login(self, email=None, password=None):
        if email is None or password is None:
            email = 'hzj.com'
            password = '123'
        with app.app_context():
            response = self.client.post('/users/login',
                                        data=json.dumps(dict(email=email, password=password)),
                                        content_type='application/json')
            data = response.get_json()
            # self.assertIn("login", data)
            login = data['login']
            self.assertEqual(login, True)

    def test_fail_login(self, email="wrong-email", password="wrong-password"):
        with app.app_context():
            response = self.client.post('/users/login',
                                        data=json.dumps(dict(email=email, password=password)),
                                        content_type='application/json', follow_redirects=True)
            data = response.get_json()
            print(data)
            # self.assertIn("login", data)
            login = data['login']
            self.assertEqual(login, False)

    def test_login_logout_user(self):
        with app.app_context():
            res1 = self.client.post('/users/login',
                         data=json.dumps(dict(email="hzj.com", password="123")),
                         content_type='application/json', follow_redirects=True)
            dat1 = res1.get_json()
            log1 = dat1['login']
            self.assertEqual(log1, True)

            response = self.client.get('/users/logout', follow_redirects=True)
            data = response.get_json()
            print(data)
            logout = data['logout']
            self.assertEqual(logout, True)

    def test_register(self, email=None, password=None, username =None):
        if email is None or password is None or username is None:
            email = 'gjf.com'
            password = '123'
            username = "gjf"
        with app.app_context():
            response = self.client.post('/users/register',
                                        data=json.dumps(dict(username=username,
                                        email=email, password=password)),
                                        content_type='application/json', follow_redirects=True)
            data = response.get_json()
            # self.assertIn("login", data)
            register = data['register']
            self.assertEqual(register, True)

            #Repeated email

    def test_reset_password(self, password1 =None, password2 = None, original_password= None):
        if password1 is None or password2 is None or original_password is None:
            original_password = '123'
            password1 = '12'
            password2 = '12'

        with app.app_context():
            # first login
            res1 = self.client.post('/users/login',
                         data=json.dumps(dict(email="hzj.com", password="123")),
                         content_type='application/json', follow_redirects=True)
            dat1 = res1.get_json()
            log1 = dat1['login']
            self.assertEqual(log1, True)

            response = self.client.post('/users/reset-password',data=json.dumps(dict(password1=password1,
                                        original_password=original_password, password2=password2)),
                                        content_type='application/json', follow_redirects=True)
            data = response.get_json()
            reset = data['reset_password']
            self.assertEqual(reset, True)

    def test_reset_username(self, new_username = None):
        if new_username is None:
            new_username = "ripley"
        with app.app_context():

            # First Without Login
            response = self.client.post('/users/reset-username',data=json.dumps(dict(new_username=new_username)),
                                        content_type='application/json', follow_redirects=True)
            data = response.get_json()
            self.assertIsNone(data)

            # Login First
            res1 = self.client.post('/users/login',
                                    data=json.dumps(dict(email="hzj.com", password="123")),
                                    content_type='application/json', follow_redirects=True)
            dat1 = res1.get_json()
            log1 = dat1['login']
            self.assertEqual(log1, True)

            # Get Method Test
            res0 = self.client.get('/users/reset-username', follow_redirects=True)
            data0 = res0.get_data(as_text=True)
            self.assertIn('reset username', data0)

            # Post Method Test
            response = self.client.post('/users/reset-username', data=json.dumps(dict(new_username=new_username)),
                                        content_type='application/json', follow_redirects=True)
            data = response.get_json()
            self.assertIsNotNone(data)
            reset = data['reset_username']
            self.assertEqual(reset, True)
            # self.assertEqual(data['reset_username'], True)


    def test_reset_email(self, new_email = None, password = "123"):
        if new_email is None:
            new_email = "ripley.com"
        with app.app_context():

            # First Without Login
            response = self.client.post('/users/reset-email',data=json.dumps(dict(new_email=new_email,password = password)),
                                        content_type='application/json', follow_redirects=True)
            data = response.get_json()
            self.assertIsNone(data)

            # Login First

            res1 = self.client.post('/users/login',
                                    data=json.dumps(dict(email="hzj.com", password=password)),
                                    content_type='application/json', follow_redirects=True)
            dat1 = res1.get_json()
            log1 = dat1['login']
            self.assertEqual(log1, True)

            # Get Method Test
            res0 = self.client.get('/users/reset-email', follow_redirects=True)
            data0 = res0.get_data(as_text=True)
            self.assertIn('Welcome to reset email', data0)

            # Post Method Test

            # Password fail
            response = self.client.post('/users/reset-email', data=json.dumps(dict(new_email=new_email, password = "12")),
                                        content_type='application/json', follow_redirects=True)
            data = response.get_json()
            reset = data['reset_email']
            self.assertEqual(reset, False)

            # Email does not change
            response1 = self.client.post('/users/reset-email', data=json.dumps(dict(new_email="hzj.com", password="123")),
                                        content_type='application/json', follow_redirects=True)
            data1 = response1.get_json()
            reset1 = data1['reset_email']
            self.assertEqual(reset1, False)

            # Success
            response2 = self.client.post('/users/reset-email',
                                         data=json.dumps(dict(new_email=new_email, password="123")),
                                         content_type='application/json', follow_redirects=True)
            data2 = response2.get_json()
            reset2 = data2['reset_email']
            self.assertEqual(reset2, True)

        def test_return_user_info(self, email = "hzj.com", password = "123"):
            with app.app_context():

                # login first
                res1 = self.client.post('/users/login',
                                        data=json.dumps(dict(email=email, password=password)),
                                        content_type='application/json', follow_redirects=True)
                dat1 = res1.get_json()
                log1 = dat1['login']
                self.assertEqual(log1, True)

                response = self.client.get('/users/info',follow_redirects=True)
                data = response.get_json()

                username = data['username']
                return_email = data['email']
                self.assertEqual(username, "hzj")
                self.assertEqual(return_email, "hzj.com")

# Basic view function test
    def test_404_page(self):
        # 测试404错误
        response = self.client.get('/nothing') #随便写一个未定义的url
        data = response.get_data(as_text=True)
        self.assertIn('this page does not exist', data)
        # self.assertIn('Go Back', data)
        self.assertEqual(response.status_code, 404)

    def test_401_page(self):
        response = self.client.get('/UnauthorizedPage')
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized permission to this page', data)

    def test_index_page(self):
        response = self.client.get('/firstpage')
        data = response.get_data(as_text=True)
        self.assertIn('Hello, world!', data)



    # def test_create_user(self):
    #     response = self.client.post('/', data= json
    #     ), follow_redirects=True)
    #     data = response.get_data(as_text=True)
    #     self.assertIn('Your message have been sent to the world!', data)
    #     self.assertIn('Hello, world.', data)
    #
    # def test_form_validation(self):
    #     response = self.client.post('/', data=dict(
    #         name=' ',
    #         body='Hello, world.'
    #     ), follow_redirects=True)
    #     data = response.get_data(as_text=True)
    #     self.assertIn('This field is required.', data)
    #
    # def test_forge_command(self):
    #     result = self.runner.invoke(forge)
    #     self.assertIn('Created 20 fake messages.', result.output)
    #     self.assertEqual(Message.query.count(), 20)
    #
    # def test_forge_command_with_count(self):
    #     result = self.runner.invoke(forge, ['--count', '50'])
    #     self.assertIn('Created 50 fake messages.', result.output)
    #     self.assertEqual(Message.query.count(), 50)


# Command test
    def test_initdb_command(self):
        result = self.runner.invoke(initdb) #对程序实例app调用test_cli_runner（),会返回一个FlaskCliRunner
        self.assertIn('Initialized database.', result.output)
# 使用FlaskCliRunner提供的invoke（）方法调用命令，传入命令函数对象作为第一个参
# 数。invoke（）调用会返回一个包含命令执行结果的Result对象，其中
# 的output属性包含命令的输出内容。通过判断命令的输出字符和数据库
# 的记录数量，我们就可以判断这个功能是否正常。


    def test_initdb_command_with_drop(self):
        result = self.runner.invoke(initdb, ['--drop'], input='y\n')
        self.assertIn('This operation will delete the database, do you want to continue?', result.output)
        self.assertIn('Drop tables.', result.output)
# 新生成数据库的initdb命令在使用--drop选项后，会给出确认提示，我们
# 需要在invoke（）方法中使用input参数给出输入值

if __name__ == '__main__':
    unittest.main()
