AnonChat
========

Installation Instructions
-------------------------

### Prerequisites:
1. Python (2.7 or 3.4+ should work)
   * pip and virtualenv should be installed
1. PostgreSQL (not sure which version, I'm working with 9.5.1)
1. Google's Chrome web browser (I've tested this with IE and Chrome, and it only works with Chrome for some reason)

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
   1. Run the db_setup.sql against the PostgreSQL instance so the database is created and then all objects are created within the database. I'm not sure how to do this, but I feel like it should be possible.
1. `python app.py`
1. Using Google Chrome, navigate to [http://localhost:5000](http://localhost:5000)

------------

#### A little about this solution:

##### A brief walk-through of the architecture:

On Startup, the app allocates the necessary resource locaters (any line that starts with `@app.route(` is defining a resource locater in Flask), opens and reads the required template files (now from os independent paths!), and gets the database connections. In my opinion, these should be cached so that they don't have to be created every time a user makes a request to a server.

When the user makes a request to the root url of the application, the application returns the static page that (should) look a lot like wireframe 1. The user should put in a username that they want to chat with, and this should take them to the second wireframe. *Technical note:* In the background, this is not verified by the server. The button click redirects the browser from the current page to the next page using javascript. Is this a great way to accomplish this goal? No. Does it work? Yes.

The second page is more interesting. Initially it looks like the first page, with a text box and a button that has almost the exact same functionality as the front page's button. However, the server will also populate the page with a list of users that the user has corresponded with in the past. *Technical notes:* Button on this page works exactly like the button on the front page (redirect with javascript). Again, not great, but functional. The list of links is concatenated directly into the page, so if a malicious user attempts to use this, they can execute arbitrary code on the client machine. A lot of this app was made with the assumption of non-malicious users. This text can be sent through an XSS filter (like the one included in Flask) to defeat XSS attack here.

The third page is probably the most complicated of the bunch, containing several javascript functions and the only real communication back to the server. The chat messages are sent to the server using a POST method (PUT could have been used, and I would only have to change all instances of POST to PUT). The code for sending the messages to the server are directly on the chat_screen.html page. The error handling code is not as robust as it should be, but again, this was done quickly. Once per second, the browser sends a GET request to the sever to get the current chat log between the users listed in the url. This gets the full chat log, which would need to be fixed if this would be productized. *Technical notes:* The GET request is far heavier than it needs to be. I was going to make a 'new' endpoint so that users can get just the new messages on their conversations, but that would be quite hard, and require validating the users as they're getting the messages (they couldn't just do GET host/user/with/user2/new, there would have to be some way to verify that the user had seen the message before. Something like timestamping, which would grow the complexity to be far larger than it is right now). I'm sort of happy with how the post request turned out. If the app is run on a server with SSL certification, even if there's a MITM attack, the attacker should only be able to see who's corresponding with whom, and not the content of the messages.

##### A list of TODOs and regrets:

This took WAY longer than it should have. I probably spent about 6 - 8 hours on this, and I would have far preferred to spend the recommended 2 - 3 hours on it. I had more issues connecting to the database than I expected, and I spent more time messing with the callbacks on the HTML pages than I should have.

If I had more time, I would improve the security on the application. Currently, I don't think this is vulnerable to SQL injection attacks (yay, parameterized queries!), but there's some real danger of XSS attacks (putting unescaped text directly into the page = bad news for users). There are some simple libraries for this, including one included with Flask (the platform that I'm using for this app), but I didn't have time to look deeply into it.

It should be trivial to move the callbacks for posting and getting messages to their own top-level functions, but I wasn't able to. I would spend some time to clean this up.

I'm mixing username and user id in the main app right now. I would like to move everything to user id so that we only have to get the user id at the start of a transaction and then we can use it through the rest of the transaction. I think that would be better.

Given some extra hours, I would also include a queue so that users don't have to download the entire chat every time they want to get new messages.

This looks like butt. It really needs to be prettied up.

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
