import csv, os, time, datetime

public = 'public/'
private = 'private/'

class chatObject:
    def __init__(self, sender: str, message: str, time: int = int(time.mktime(datetime.datetime.utcnow().timetuple())*1000)):
        self.sender  = sender
        self.message = message
        self.time    = time
        self.id      = str(hash(str(self)))[1:16]

    def __str__(self):
        return f'{self.sender} said {self.message} at {self.time}'

    def __repr__(self):
        return f'chatObject({self.sender}, {self.message}, {self.time})'

    def getId(self):
        return self.id

    def getChat(self):
        return {
            "sender":self.sender,
            "message":self.message,
            "time":self.time,
            "id":self.id
        }

def checkLogin(login: dict) -> bool:
    '''
    Master Login code
    '''
    user = getUserLogin(login['uname'])
    if user == None:
        return user
    else:
        return (checkPass(login['pass'], user['hash']))

def validUser(currentUsers, toValidate):
    return currentUsers[toValidate['uname']] == toValidate['cookie']

def giveCookie():
    return str(hash(os.urandom(60)))

def getUserLogin(name: str) -> dict:
    with open(private + 'pass.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (row['name'] == name):
                return row
    return None

def  makeLogin(request) -> str:
    '''
    Makes login
    '''
    login = {'uname':request.get('uname'),'pass':request.test.get('pass1')}
    if (login['pass'] == request.get('pass2')):
        if (getUserLogin(login['uname']) != None):
            return False
        with open(private + 'pass.csv', 'a') as file:
            file.write(','.join([login['uname'],hashword(login['pass'])]) + '\n')
        return '/'
    return '/html/chat/signup.html'

import hashlib
import binascii

def checkPass(userPassword: str, verifiedPassword: str) -> bool:
    '''
    Checks the userPassword against the verifiedPassword
    Pass user, then verified
    '''
    return hashword(userPassword, verifiedPassword[:64].encode('ascii')) == verifiedPassword

def hashword(password: str, salt: str = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')) -> str:
    '''
    Makes the password hash
    Pass user password to make new pass
    Pass salt to get same salt
    '''
    pwdhash = binascii.hexlify(hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000))
    return (salt + pwdhash).decode('ascii')

import fileinput

def replacePassphrase(uname, oldPass, newPass1, newPass2):
    print(uname, oldPass, newPass1, newPass2)
    if not ((newPass1 == newPass2) and (checkLogin({ 'uname': uname, 'pass': oldPass }))):
        return False
    for line in fileinput.FileInput(private + "pass.csv", inplace=True):
        if line[:len(uname)] == uname:
            print(uname + ',' + hashword(newPass1) + '\n', end='')
        else:
            print(line, end='')
    return True
