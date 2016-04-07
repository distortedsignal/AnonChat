from flask import Flask
app = Flask(__name__)

@app.route("/")
def main_page():
    # Return a static HTML page
    return front_page

@app.route("/<username>")
def user_page(username):
    # If this was real, I would want this to be architected in a radically 
    # different fashion. Login should happen on the server, not as a get 
    # request from the client. At a minimum, this should be a post request and 
    # run any password given against an excellent password hashing function 
    # with a generous work factor (naturally, I would include a large, random 
    # salt in the database on a per-user basis)
    pass

@app.route("/<username>/with/<other_username>")
def text_page(username, other_username):
    pass

@app.route("/<username>/with/<other_username>/new")
def new_messages(username, other_username):
    pass

if __name__ == "__main__":
    front_page = open('html_templates\\login.html').read()
    app.run()
