import bottle

app = bottle.Bottle()
serverIP = 'localhost' # Your IP here, or localhost for your machine only
serverPort = '8080' # Ports 1-1024 need admin access on linux to host

@app.route('/<filepath:path>') # This is the line where you specify what would go after your IP, so localhost/<filename>
def server_static(filepath):
    return bottle.static_file(filepath, root='./public') # Root is where to get the files from locally

@app.route('/') # Specific case
def rootDirector():
    bottle.redirect('/index.html')  # Redirects      

@app.route('/<message:path>', method="post") # You can use POST to do stuff server side
def index_button(message):
    print(message) # Will print the post in local console

application = bottle.default_app() # For server running site, like pythonanywhere.com

if __name__ == "__main__":
    bottle.run(app, host=serverIP, port=serverPort) # Locally run site