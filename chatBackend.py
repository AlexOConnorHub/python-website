# Imports
import bottle, chat, os, json, re
from gevent import monkey; monkey.patch_all()
from time import time

# Constants
serverIP = 'localhost'
serverPort = '8080'
public = 'public/'
private = 'private/'
historySize = 50

# Variables
updateBool = True
updateTime = time()
valid = {}

# On load, get last {historySize} chats
fileIO = open(private + 'history.bk', 'r')
sendChat = [chat.chatObject(json.loads(line)['sender'], json.loads(line)['message'], 
json.loads(line)['time']) for line in fileIO.read().split('\n')]
fileIO.close()

# On load, make banned words list
fileIO = open(private + 'profane.bad', 'r')
profane = json.loads( open(private + 'profane.bad', 'r').read())
fileIO.close()

# Chating
@bottle.route('/chat/message', method="POST")
def chatPost():
    return makeChat(eval(bottle.request.body.read().decode('utf8')))

#Tell others
@bottle.route('/update')
def sendToPeople():
    bottle.response.content_type = 'text/event-stream'
    yield advertise()

# Give to others
@bottle.route('/chat/<id:int>', method="POST")
def giveChat(id):
    return getChat(id)

# On page loading
@bottle.route('/chat/onload', method="POST")
def pageLoad():
    return findAllChats()

# Change Login info
@bottle.route('/change', method="POST")
def change():
    chat.replacePassphrase(bottle.request.forms.get('uname'),
    bottle.request.forms.get('oldPass'), bottle.request.forms.get('newPass1'),
    bottle.request.forms.get('newPass2'))
    return bottle.redirect('/html/chat/account.html')

# Login
@bottle.route('/login', method="POST")
def login():
    return makeCookie(eval(bottle.request.body.read().decode('utf8')))

# Upload photo
@bottle.route('/upload', method='POST')
def do_upload():
    state = saveFile(bottle.request)
    return bottle.redirect('/html/chat/account.html')

# Sign up
@bottle.route('/signup', method='POST')
def signup():
    bottle.redirect(chat.makeLogin(bottle.request.forms))

# Run
application = bottle.default_app()

# Functions using global Variables
def makeChat(message):
    global updateBool, updateTime, sendChat, valid
    state = {"state":(valid[message['sender']] == message['cookie']) and isClean(message['message'])}
    if state['state']:
        tempChat = chat.chatObject(message['sender'], message['message'])
        if len(sendChat) >= historySize:
            sendChat = sendChat[1:]
        sendChat.append(tempChat)
        fileIO = open(private + 'history.bk', 'w')
        for mess in sendChat:
            fileIO.write(json.dumps(mess.getChat()))
            if not(mess == tempChat):
                fileIO.write('\n')
        fileIO.close()
        updateBool = True
        updateTime = time()
    return state

def advertise():
    global updateBool, updateTime, sendChat
    final =  'retry: 4000\n\n'
    if ((time() - updateTime) > 5):
        updateBool = False
    if updateBool:
        for mess in sendChat:
            final += f'data: ' + str(mess.getId()) + '\n'
        final += '\n'
    return final

def findAllChats():
    global sendChat
    final = {}
    count = 0
    for mess in sendChat:
        if (mess != ''):
            final[count] = str(mess.getId())
        count += 1
    return final

def getChat(id):
    global sendChat, valid
    message = eval(bottle.request.body.read().decode('utf8'))
    final = {'state' : False}
    if (valid[message['uname']] == message['cookie']):
        for mess in sendChat:
            if int(mess.getId()) == id:
                final = mess.getChat()
                final['state'] = True
                break
    return final

def makeCookie(message):
    global valid
    state = chat.checkLogin(message)
    cookie = 0
    if state:
        cookie = chat.giveCookie()
        valid[message['uname']] = cookie
    final = {'state':state, 'cookie':cookie}
    return final

def isClean(message):
    for word in re.sub('[-_/.~,?!@#]', ' ', message).split(' '):
        if word.lower() in profane:
            return False
    return True

def saveFile(request):
    global valid
    if (valid[request.forms.uname] == request.forms.cookie):
        upload = request.files.get('upload')
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.png', '.jpg', '.jpeg'):
            return False
        upload.filename = request.forms.uname + ext
        upload.save( public + 'images/profile', True)
    return True

if __name__ == "__main__":

    # Public folder
    @bottle.route('/<filepath:path>')
    def server_static(filepath):
        return bottle.static_file(filepath, root=public)
        
    bottle.run(server=bottle.GeventServer, host=serverIP, port=serverPort, debug=True)