from flask import Flask, abort, url_for, request, render_template, session, redirect
from builtins import zip

app = Flask(__name__)

### This is the secret key necassary for using the 'session' function.
app.config['SECRET_KEY'] = 'secret'

### Lists which are used to store the posts' data.
posts = []
postnames = []
postcitys = []
postpics = []
post_data = []


### Main index page.
@app.route('/')
def index(methods=['GET', 'POST']):

    ### Sets default values for the username, profile picture and location.
    session.setdefault('nameField', 'Anonymous')
    session.setdefault('profilePic', 'static/img/ppdefault.png')
    session.setdefault('cityField', ' ')  

    ### Tells the system where to retrieve the updated name, profile picture and location.
    name = session['nameField']
    picture = session['profilePic']
    city = session['cityField']
    
    return render_template('index.html', post_data=post_data, zip=zip, username=name, ppic=picture, myCity=city, posts=posts, postnames=postnames)


### Retrieves the user's name, profile picture and location for the Menu page.
@app.route('/menu', methods=['GET'])
def menu():
    name = session['nameField']
    picture = session['profilePic']
    city = session['cityField']
  
    return render_template('menu.html', username=name, ppic=picture, myCity=city)


### Gives the user a 404 error page with a custom message if the URL is incorrect.
@app.errorhandler(404)
def page_not_found(error):
    return "You went to the wrong page :(", 404


### The function used to submit posts and have them displayed on the index page.
@app.route('/', methods=['GET', 'POST'])
def posting():

    ### Retrieves the user's name, profile picture and location.
    name = session['nameField']
    picture = session['profilePic']
    city = session['cityField']

    ### Retrieves the text inputted into the post input box.
    post = request.form['postText']

    ### Declares the variables used for the lists which store the post data.
    postname = name
    postcity = city
    postpic = picture

    ### If a post hasn't been entered but is submitted a prompt will be shown to the user to ask them to write something.
    if not post:
        error = "Please enter something before posting"
        return render_template('index.html', error=error, username=name, ppic=picture, myCity=city, posts=posts, postnames=postnames)

    ### If a post has been created; add the correct information to their correrlating lists.
    else:
        posts.append(post)
        postnames.append(postname)
        postcitys.append(postcity)
        postpics.append(postpic)

        ### Combines the lists into one so that the posts and posting data (such as username etc.) can be easily linked together.
        post_data = list(zip(posts, postnames, postcitys, postpics))

    return render_template('index.html', post_data=post_data, zip=zip, username=name,  ppic=picture, myCity=city, posts=posts, postnames=postnames)
   

### Handles the POST request used for when a user wishes to enter or change their personal information.
@app.route("/menu", methods =['POST'])
def handle_post_request():
 
    ### Retrieves the user's name, profile picture and location.
    name = request.form['nameField']
    city = request.form['cityField']
    picture = request.form['profilePic']

    ### If the user did not choose a profile picture they will be met with an error message.
    if picture is None or picture  == '':
        error = "Please select a profile picture before continuing."
        return render_template('menu.html', error=error)

    ### Sets the user's session name, profile picture and location to the information they entered into the page.
    session['nameField'] = name
    session['cityField'] = city
    session['profilePic'] = picture

    return render_template('menu.html', post_data=post_data, zip=zip, username=name, ppic=picture, myCity=city, posts=posts, postnames=postnames)


### A function which allows the user to clear the current session data by using the '/clear' URL.
@app.route("/clear")
def clear_session():
    session.clear()
    return "Session data cleared"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
