import os
import unittest
 
from flaskblog import app, db, mail
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
        # Disable sending emails during unit testing
        mail.init_app(app)
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass


#### basic operations ####
    
    def register(self, username, email, password, confirm_password):
        return self.app.post(
            '/register',
            data=dict(username = username, email = email, password = password, confirm_password = confirm_password),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def account(self):
        return self.app.get(
            '/account',
            data=dict(),
            follow_redirects=True
        )
        

 
###############
#### tests ####
###############

# main page
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True) # 发送请求
        self.assertEqual(response.status_code, 200) # 接收信号

# register
    def test_valid_user_registration(self): # 正确登录
        response = self.register('Tom', '1013752750@qq.com', 'TheFirstPassword', 'TheFirstPassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn( b'Your account has been created!' , response.data)

    def test_invalid_user_registration_different_passwords(self): # 前后密码不一致
        response = self.register('Tom', '1013752750@qq.com', 'TheFirstPassword', 'TheDifferentPassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be equal to password.', response.data)

    def test_invalid_user_registration_duplicate_email(self):
        response = self.register('Tom', '1013752750@qq.com', 'TheFirstPassword', 'TheFirstPassword')
        self.assertEqual(response.status_code, 200)
        response = self.register('AnotherTom', '1013752750@qq.com', 'TheFirstPassword', 'TheFirstPassword')
        self.assertIn(b'That email is taken. Please choose a different one.', response.data)

    def test_invalid_user_registration_duplicate_username(self):
        response = self.register('Tom', '1013752750@qq.com', 'TheFirstPassword', 'TheFirstPassword')
        self.assertEqual(response.status_code, 200)
        response = self.register('Tom', '1013752750@gmail.com', 'TheFirstPassword', 'TheFirstPassword')
        self.assertIn(b'That username is taken. Please choose a different one.', response.data)

# login
    def test_valid_login(self): # 正确登录
        response = self.register('Tom', '1013752750@qq.com', 'TheFirstPassword', 'TheFirstPassword')
        self.assertEqual(response.status_code, 200)
        response = self.login('1013752750@qq.com', 'TheFirstPassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn( b'Login successfully' , response.data)

    def test_invalid_login_wrong_email_format(self):
        response = self.login('1013752750', 'TheFirstPassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn( b'Invalid email address' , response.data)

    def test_invalid_login_no_such_email(self):
        response = self.login('Null@null.com', 'TheFirstPassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn( b'Login Unsuccessful. Please check email and password' , response.data)

    def test_invalid_login_wrong_password(self):
        response = self.register('Tom', '1013752750@qq.com', 'TheFirstPassword', 'TheFirstPassword')
        self.assertEqual(response.status_code, 200)
        response = self.login('1013752750@qq.com', 'TheWrongPassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn( b'Login Unsuccessful. Please check email and password' , response.data)

# logout
    def test_user_logout(self):
        response = self.register('Tom', '1013752750@qq.com', 'TheFirstPassword', 'TheFirstPassword')
        self.assertEqual(response.status_code, 200)
        response = self.login('1013752750@qq.com', 'TheFirstPassword')
        self.assertEqual(response.status_code, 200)
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn( b'Successfully Logout !' , response.data)

        

if __name__ == "__main__":
    unittest.main()
