from __future__ import print_function
from flask import Flask, request

import traceback
import psycopg2
import sys
import os

app = Flask(__name__)

# TODO change username to user id everywhere

def get_db_connections():
    # Why do we need so many connections? So that we can harshly limit the
    # permissions of each connection. For example, chat partners should only
    # be able to access the table that relates usernames and ids, and the table
    # of which user ids have had conversations. It should be able to modify both
    # of these tables. If I was really paranoid, I would want to make a 
    # connection that was exclusively allowed to add users.
    # The chat history should be the only connection that is able to read a
    # conversation from the database.
    # The post message connection should be the only connection to write to the
    # conversations table
    conn_string_template = "host='HOST_NAME' dbname='DATABASE_NAME' \
    user='USERNAME' password='PASSWORD'"
    # Assume the database is on the same machine as the server, assume the 
    # database name is "AnonChat_db"
    conn_string_template = conn_string_template.replace('HOST_NAME', 
        'localhost').replace('DATABASE_NAME', 'AnonChat_db')
    connection_map = {}
    connection_map['chat_partners'] = psycopg2.connect(
        conn_string_template.replace('USERNAME', 'chat_partners').replace(
            'PASSWORD', 'chat_partners_password'))
    connection_map['get_history'] = psycopg2.connect(
        conn_string_template.replace('USERNAME', 'get_history').replace(
            'PASSWORD', 'get_history_password'))
    connection_map['post_message'] = psycopg2.connect(
        conn_string_template.replace('USERNAME', 'post_message').replace(
            'PASSWORD', 'post_message_password'))

    return connection_map

def get_user_id(username, connection):
    # Non-pure code
    cursor = connection.cursor()
    cursor.execute('Select id from public.users where username = %s',
        (username,))
    records = cursor.fetchall()
    # This may introduce a race condition, but I'm not sure.
    if not records:
        # This user is new
        print("Adding user '" + username + "'")
        cursor.execute('Insert into public.users (username) VALUES (%s)',
            (username,))
        connection.commit()
        cursor.execute('Select id from public.users where username = %s',
            (username,))
        records = cursor.fetchall()
    # The records method is guaranteed to have at least one id in it now.
    cursor.close()
    return records[0]

def get_two_user_ids(username, other_username, connection):
    return [get_user_id(username, connection), get_user_id(other_username, 
        connection)]

def get_partners_list(user_id, connection):
    cursor = connection.cursor()
    cursor.execute('select username from public.users where id in (select \
        second_id from public.user_connections where id = %s)', (user_id,))
    records = cursor.fetchall()
    cursor.close()
    return records

def render_user_page(request, chat_partners):
    # request.path should be the full user home page url
    link_start = '<a href="' + request.path + '/with/'
    link_middle = '">'
    link_end = '</a><br>'

    # This is a sloppy map/reduce where the map is "create a list of links" and
    # the reduce is "concatenate those links together in a string."
    link_collation = ''.join(
        map(
            lambda x: link_start + x[0] + link_middle + x[0] + link_end, 
            chat_partners)
        )

    # Yes, yes, XSS, I know, I would replace this with an actual template and
    # XSS defeating filter if I had the time.
    return user_home_page.replace('{{chat_partners}}', link_collation)

def has_history(user_id, other_user_id, connection):
    # To speed this function up, move the get user id logic into the SQL statement.
    cursor = connection.cursor()
    cursor.execute('select * from public.user_connections where id = %s and \
        second_id  = %s', (user_id, other_user_id))
    results = cursor.fetchall()
    cursor.close()
    return results

def add_history(user_id, other_user_id, connection):
    # Again, to speed this up, move this logic into the sql block that uses it.
    # Very non-pure block of code
    cursor = connection.cursor()
    # This is a terrible way to do this, but I don't want to commit the time to
    # make it better.
    cursor.execute('insert into public.chat_log (chat_text) VALUES (\'Start chatting\')')
    connection.commit()
    cursor.execute('select id from public.chat_log where chat_text = \'Start chatting\'')
    new_chat_id = cursor.fetchall()[0]
    cursor.execute('insert into public.user_connections \
        (id, second_id, chat_id) VALUES \
        (%s,      %s,            %s), \
        (   %s,            %s,      %s)', # The spacing here worked out well-ish
        (user_id, other_user_id, new_chat_id,
            other_user_id, user_id, new_chat_id))
    connection.commit()
    cursor.close()

def get_chat_history(user_id, other_user_id, connection):
    cursor = connection.cursor()
    cursor.execute("select chat_text from public.chat_log where id in \
        (select chat_id from public.user_connections where id = %s and \
            second_id = %s)", (user_id, other_user_id))
    text = cursor.fetchall()[0][0]
    cursor.close()
    return text

def render_chat_page(user_id, other_user_id, connection):
    chat_history = get_chat_history(user_id, other_user_id, connection)
    # Before running this in production, sanatize the chat history string.
    return chat_page.replace('{{chat_history}}', str(chat_history))
    pass
    
def add_chat_history(user_id, other_user_id, new_chat, connection):
    # Again, not pure code.
    cursor = connection.cursor()
    cursor.execute('update public.chat_log set chat_text = %s where id in \
        (select chat_id from public.user_connections where id = %s and \
            second_id = %s)', (new_chat, user_id, other_user_id))
    connection.commit()
    cursor.close()

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
    try:
        user_id = get_user_id(username, connection_map['chat_partners'])
        chat_partners = get_partners_list(user_id, connection_map['chat_partners'])
        return render_user_page(request, chat_partners)
    except:
        traceback.print_exc(file=sys.stdout)

@app.route("/<username>/with/<other_username>")
def text_page(username, other_username):
    try:
        user_id, other_user_id = get_two_user_ids(username, other_username, 
            connection_map['get_history'])
        # has history returns a list.
        if not has_history(user_id, other_user_id, 
                connection_map['get_history']):
            add_history(user_id, other_user_id, connection_map['get_history'])
        return render_chat_page(user_id, other_user_id, 
            connection_map['get_history'])
    except:
        traceback.print_exc(file=sys.stdout)
    
@app.route("/<username>/with/<other_username>/new", methods=['POST'])
def new_messages(username, other_username):
    try:
        user_id, other_user_id = get_two_user_ids(username, other_username, 
            connection_map['post_message'])
        if not has_history(user_id, other_user_id, 
                connection_map['post_message']):
            add_history(user_id, other_user_id, connection_map['post_message'])
        chat_history = get_chat_history(user_id, other_user_id, 
            connection_map['post_message'])
        # This is a less safe way to do this - figure out some way to do this in SQL
        chat_history += '\n' + username + ': ' + request.data.decode("utf-8")
        add_chat_history(user_id, other_user_id, chat_history,
            connection_map['post_message'])
        return ''
    except:
        traceback.print_exc(file=sys.stdout)

@app.route("/<username>/with/<other_username>/chat")
def get_chat(username, other_username):
    try:
        user_id, other_user_id = get_two_user_ids(username, other_username, 
            connection_map['post_message'])
        return get_chat_history(user_id, other_user_id, connection_map['get_history'])
    except:
        traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    # I'm opening these files and holding them in program memory because I 
    # don't want to have the penalty of "load this file" on every call to the 
    # app. This is mainly driven by the charts in this article:
    # http://blog.codinghorror.com/the-infinite-space-between-words/
    front_page = open('html_templates' + os.sep + 'login.html').read()
    user_home_page = open('html_templates' + os.sep + 'user_home_page.html').read()
    chat_page = open('html_templates' + os.sep + 'chat_screen.html').read()
    connection_map = get_db_connections()
    app.run()
