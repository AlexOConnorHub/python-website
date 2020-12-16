# Imports
import bottle, chat, os
from gevent import monkey; monkey.patch_all()
from time import time

# Import other modules
import chatBackend

# Constants
serverIP = '192.168.10.59'
serverPort = '8080'
public = 'public/'
private = 'private/'

# Variables
updateBool = True
updateTime = time()
sendChat = []
valid = {}

# Public folder
@bottle.route('/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root=public)

# Downloads
@bottle.route('/download/<filename:path>')
def download(filename):
    return bottle.static_file(filename, root=public, download=filename)

# Home page
@bottle.route('/')
def rootDirector():
    bottle.redirect('/index.html')

# Run
application = bottle.default_app()

if __name__ == "__main__":
    bottle.run(server=bottle.GeventServer, host=serverIP, port=serverPort, debug=True)