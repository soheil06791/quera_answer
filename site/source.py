import string
import hashlib
import re
import functools



class Site:
    def __init__(self, url_address):
        self.url = url_address
        self.register_users = []
        self.active_users = []
        
    def show_users(self):
        pass

    def register(self, user):
        if self.register_users:
            users_id = [user.user_id for user in self.register_users]
            if user in users_id:
                raise Exception('user already registered')
        self.register_users.append(user)
        return 'register successful'
      
    def login(self, **kwargs):
        if self.register_users:
            user_name = [user.username for user in self.register_users]
            email = [user.email for user in self.register_users]
        if 'password' in kwargs and email and user_name:
            if 'email' in kwargs and kwargs['email'] in email and 'username' in kwargs and kwargs['username'] in user_name:
                input_password = hashlib.sha256(kwargs['password'].encode(encoding='utf-8')).hexdigest()
                if input_password == self.register_users[email.index(kwargs['email'])].password:
                    if self.register_users[email.index(kwargs['email'])] in self.active_users:
                        return 'user already logged in'
                    self.active_users.append(self.register_users[email.index(kwargs['email'])])
                    return 'login successful'
            elif 'email' in kwargs and kwargs['email'] in email:
                input_password = hashlib.sha256(kwargs['password'].encode(encoding='utf-8')).hexdigest()
                if input_password == self.register_users[email.index(kwargs['email'])].password:
                    if self.register_users[email.index(kwargs['email'])] in self.active_users:
                        return 'user already logged in'
                    self.active_users.append(self.register_users[email.index(kwargs['email'])])
                    return 'login successful'
            elif 'username' in kwargs and kwargs['username'] in user_name:
                input_password = hashlib.sha256(kwargs['password'].encode(encoding='utf-8')).hexdigest()
                if input_password == self.register_users[email.index(kwargs['username'])].password:
                    if self.register_users[email.index(kwargs['email'])] in self.active_users:
                        return 'user already logged in'
                    self.active_users.append(self.register_users[email.index(kwargs['username'])])
                    return 'login successful'
        raise Exception('invalid login')


    def logout(self, user):
        if user in self.active_users:
            self.active_users.remove(user)
            return 'logout successful'
        raise Exception('user is not logged in')
        

    def __repr__(self):
        return "Site url:%s\nregister_users:%s\nactive_users:%s" % (self.url, self.register_users, self.active_users)

    def __str__(self):
        return self.url


class Account:
    def __init__(self, username, password, user_id, phone, email):
        self.username = self.username_validation(username)
        self.password = self.password_validation(password)
        self.user_id = self.id_validation(user_id)
        self.phone = self.phone_validation(phone)
        self.email = self.email_validation(email)
        
    def set_new_password(self, password):
        upper = False
        lower = False
        number = False
        number_check = '0123456789'
        if len(password) < 8:
            raise Exception('invalid password')
        
        for i in password:
            if i in string.ascii_lowercase:
                lower = True
            elif i in string.ascii_uppercase:
                upper = True
            elif i in number_check:
                number = True
            if upper and lower and number:
                print('ok')
                self.password = hashlib.sha256(password.encode(encoding='utf-8')).hexdigest()
                return 
        raise Exception('invalid password')

        
        
        

    def username_validation(self, username):
        if '_' not in username or len([i for i in username if i == '_']) > 1:
            raise Exception('invalid username')
        return username

    def password_validation(self, password):
        upper = False
        lower = False
        number = False
        number_check = '0123456789'
        if len(password) < 8:
            raise Exception('invalid password')
        
        for i in password:
            if i in string.ascii_lowercase:
                lower = True
            elif i in string.ascii_uppercase:
                upper = True
            elif i in number_check:
                number = True
            if upper and lower and number:
                password = hashlib.sha256(password.encode(encoding='utf-8')).hexdigest()
                return password

        raise Exception('invalid password')



    def id_validation(self, id):
        code_id = list(map(int, str(id)))[::-1]
        if len(code_id) != 10:
            raise Exception('invalid code melli')
        aggrate_id  = sum([code_id[i]*(i+1) for i in range(10) if i != 0])
        print(aggrate_id)
        remain_id =aggrate_id%11
        if remain_id<2:
            if remain_id == code_id[0]:
                return id
        else:
            if 11-remain_id == code_id[0]:
                return id
        raise Exception('invalid code melli')


    def phone_validation(self, phone):
        if '+' in phone:
            phone = phone.replace('+','')
        phone_num = list(map(int, str(phone)))

        if len(phone_num) == 11:
            if not list(set([0,9])-set(phone_num[:2])):
                return phone
        elif len(phone_num) == 13:
            if not list(set([9,8,9])-set(phone_num[:3])):
                phone=''.join(phone_num[2:].insert(0,0))
                return phone
        raise Exception('invalid phone number')


    def email_validation(self, email):
        check_email =  re.search(r'(?i)^[a-zA-Z0-9-_.]+\@?[a-zA-Z0-9-_.]+\.[a-zA-Z]{2,5}$', email)
        if check_email:
            return email
        raise Exception('invalid email')

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username


def show_welcome(func):
    @functools.wraps(func)
    def wrraper(user):
        if len(user.username) > 15:
            user = user.username[:16]+'...'
        else:
            user = user.username
        user_name = user.split('_')
        user_name[0] = user_name[0].capitalize()
        user_name[1] = user_name[1].capitalize()
        user_name.insert(1,' ')
        return func(''.join(user_name))
    return wrraper


def verify_change_password(func):
    @functools.wraps(func)
    def wrraper(*args):
        user, old_pass, new_pass = args
        if user.password != hashlib.sha256(old_pass.encode(encoding='utf-8')).hexdigest():
            raise Exception('invalid old password')
        user.set_new_password(new_pass)
        return func(user, old_pass, new_pass)
    return wrraper
        
    
@show_welcome
def welcome(user):
    return ("welcome to our site %s" % user)

@verify_change_password
def change_password(user, old_pass, new_pass):
    return ("your password is changed successfully.")

