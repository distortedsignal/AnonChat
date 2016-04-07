from flask import Flask

import psycopg2

app = Flask(__name__)

def get_db_connections():
    conn_string_template = "host='HOST_NAME' db_name='DATABASE_NAME' user='USERNAME' password='PASSWORD'"
    # Assume the database is on the same machine as the server, assume the database name is "AnonChat_db"
    conn_string_template = conn_string_template.replace('HOST_NAME', 'localhost').replace('DATABASE_NAME', 'AnonChat_db')
    connection_map = {}

    # Why do we need four connections? So that we can harshly limit the
    # permissions of each connection. For example, chat partners should only
    # be able to access the table that relates usernames and ids, and the table
    # of which user ids have had conversations. It should be able to modify both
    # of these tables. If I was really paranoid, I would want to make a 
    # connection that was exclusively allowed to add users.
    connection_map['chat_partners'] = psycopg2.connect(conn_string_template.replace('USERNAME', 'chat_partners').replace('PASSWORD', 'chat_partners_password'))
    # The chat history should be the only connection that is able to read a
    # conversation from the database.
    connection_map['get_history'] = psycopg2.connect(conn_string_template.replace('USERNAME', 'get_history').replace('PASSWORD', 'get_history_password'))
    # The post message connection should be the only connection to write to the
    # conversations table
    connection_map['post_message'] = psycopg2.connect(conn_string_template.replace('USERNAME', 'post_message').replace('PASSWORD', 'post_message_password'))

    return connection_map

def get_user_id(username, connection):
    # TODO
    cursor = connection.cursor()
    cursor.execute('Select id from users where username = %s', (username,))
    records = cursor.fetchall()
    # This may introduce a race condition, but I'm not sure.
    if records == None:
        # This user is new
        cursor.execute('Insert into users (username) VALUES (%s)', (username,))
        cursor.execute('Select id from users where username = %s', (username,))
        records = cursor.fetchall()
    # The records method is guaranteed to have at least one id in it now.
    cursor.close()
    return records[0]

def get_partners_list(user_id, connection):
    cursor = connection.cursor()
    cursor.execute('select username from users where id in (select second_id from user_connections where id = %s)', (user_id,))
    records = cursor.fetchall()
    cursor.close()
    return records
    
def get_chat_partners(username):
    user_id = get_user_id(username, connection_map['chat_partners'])
    return get_partners_list(user_id, connection_map['chat_partners'])

def render_user_page(request, chat_partners):
    # request.path should be the full user home page url
    link_start = '<a href="' + request.path + '/with/'
    link_middle = '">'
    link_end = '</a><br>'

    # This is a sloppy map/reduce where the map is "create a list of links" and
    # the reduce is "concatenate those links together in a string."
    link_collation = ''.join(
        map(
            lambda x: link_start + x + link_middle + x + link_end, 
            chat_partners)
        )

    # Yes, yes, XSS, I know, I would replace this with an actual template and
    # XSS defeating filter if I had the time.
    return user_home_page.replace('{{chat_partners}}', link_collation)

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
    chat_partners = get_chat_partners(username)
    return render_user_page(flask.request, chat_partners)

@app.route("/<username>/with/<other_username>")
def text_page(username, other_username):
    pass

@app.route("/<username>/with/<other_username>/new")
def new_messages(username, other_username):
    pass

if __name__ == "__main__":
    # I'm opening these files and holding them in program memory because I 
    # don't want to have the penalty of "load this file" on every call to the 
    # app. This is mainly driven by the charts in this article:
    # http://blog.codinghorror.com/the-infinite-space-between-words/
    front_page = open('html_templates\\login.html').read()
    user_home_page = open('html_templates\\user_home_page.html').read()
    connection_map = get_db_connections()
    app.run()
