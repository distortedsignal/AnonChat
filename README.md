AnonChat
========

Installation Instructions
-------------------------

### Prerequisites:
1. Python (2.7 or 3.4+ should work)
   * pip and virtualenv should be installed
1. PostgreSQL (not sure which version, I'm working with 9.5.1)

### Installation instructions:
1. `git clone https://github.com/distortedsignal/AnonChat.git`
1. `cd AnonChat`
1. `virtualenv venv`
1. Start the virtual environment
   * On Windows, `venv\Scripts\activate`
   * On Linux or OSX, `./venv/Scripts/activate` (probably? I didn't test this)
1. `pip install -r requirements.txt`
* EITHER
   1. Create a database named AnonChat_db in your PostgreSQL instance
   2. Run everything from line 11 in the db_setup.sql on to add users, sequences, and tables to the database.
* OR
   1. Run the db_setup.sql against the PostgreSQL instance so the database is created and then all objects are created within the database. I'm not sure how to do this, but I feel like it might be possible.
1. `python app.py`

------------

Instructions for 'AnonChat' take-home interview project

Overview:
Your task is to create a very simple web app, implementing both the frontend
and backend, that allows users to assume any username and chat with a user
of any other username. The web app should contain three pages, detailed in
text below and with the accompanying wireframe. The app can be written with
any language or framework you want, provided it is relatively simple for us
to run your app on our machines (which we definitely will!). The intention is
for you to spend roughly 2-3 hours on the project, with the end result being
an accurate representation of your abilities. Don't stress about having every
single detail perfect - code is never really finished! Just do your best and
try to have fun.

General Requirements:

1. Your frontend must be browser-based. We're certainly fans of native apps,
   but we're most interested in your webdev abilities.
2. Your backend must be installable and runable on either OS X, Windows (8.1
   or higher), or Linux. One additional option is to create a Vagrantfile for
   your app's backend environment, provided the base Vagrant box is publicly
   accessible.
3. You must include instructions for how to install and run your project. It
   is ok to limit the conditions your app runs in (i.e. 'this is only
   guaranteed to run on Mac OS X 10.11.x), just be explicit about it.


Specifications:

Page 1: Login
This page allows the user to specify a username and enter the system. There
are no restrictions around multiple logins - a username can be logged in
from multiple browsers/computers.  When a username is entered and the 'Login'
button is hit the user is taken to Page 2.

Page 2: Start Chat and Chat History
This page has two components:
1. The user can start a chat by manually entering a username to chat with.
   Users can initiate a chat with any other username, include names that
   have not previously been used in the system. This means that it is possible
   that the first time a username is logged-in with that username will have
   chat messages in its history. When a username is entered and the 'Chat'
   button is pressed the user is taken to Page 3, where they can chat with
   the specified other user.
2. The user can see a list of all users it has a chat history with. Clicking
   on any entry in the list will take the user to Page 3, where they can chat
   with the specified other user.

Page 3: Chat with another user
This page consists of a window of text - all previous chat messages between
the two users - and a text input for sending messages. Entering text into
the text input area sends the chat message, which should then appear in your
user's chat messages window. The recipient of the chat message should see
a chat message automatically show up in their screen after a reasonable amount
of time (on the order of seconds).
As is implied by the existence of a chat history, chat should be persistent.
As such, if this page is refreshed, all previous chat messages should appear.

How to submit your solution:
The easiest way for us is if you create an archive of your project (zip, tgz,
or some other common format) and send it to us.

FAQ:

Q: Some of the specifications aren't 100% detailed. How should I handle
   ambiguities?
A: You're certainly welcome to ask clarification questions (probably best
   to do that before you start coding), but we're equally happy for you to
   make a decision you think is right and implement it. (At Bonsai engineers
   are generally given autonomy to make decisions when lacking specific
   information, so this is representative of some situations you would
   encounter at Bonsai).

Q: Should I include some kind of unit tests with this code submission?
A: For the sake of keeping this project under 2-3 hours, no. At Bonsai we
   absolutely value testing, and we recognize that good tests take time,
   both to think through and to code. (We will ask about test design during
   the on-site interview). With that being said, it's best to make sure
   your solution works before submitting it.

Q: How nice does the UI have to look?
A: Knowing how to style a page with CSS is important, but it can be quite time
   consuming, especially if you're also fulfilling the role of the UI designer
   as well as the developer. Your end result doesn't need to look any nicer
   than the wireframe, but should look pretty close to what's represented
   there. Also, it's perfectly fine to not worry about making the layout
   responsive to screen size.

Q: Unauthenticated login seems like it would make a bad real-word product,
   so... why?
A: Mostly it's because we don't want you to spend time on boilerplate user
   signup/login/logout code. But, it also produces some product and technical
   scenarios that are a little different than usual.

Q: Should I concern myself with issues of performance or scale?
A: Not really. There's enough here just in getting everything working. (As
   with unit tests, we will ask about adapting this project for high loads
   during the on-site interview).

Q: I've worked for three hours, and though my solution isn't 100% feature
   complete I think I've demonstrated enough of my abilities. Should I
   keep going or submit what I have?
A: Submit what you have! We want to be respectful of your time, and are
   incredibly appreciative that you've given us as much of your time as you
   already have.
