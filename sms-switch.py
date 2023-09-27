from bottle import Bottle, run, route, request, static_file

import toml

import json

from pprint import pprint

app = Bottle()

with open("config.toml") as f:
    config = toml.load(f)

#
# Storing users is probably better done in a database, but as this is a demo
# I'll just store them in files on disk for now.
#

def get_users():
    return json.load(open("users.json", "r"))
    """
    Example content of users.json
    [
        {"name": "Martin", "phonenumber":"+4600000000"},
        {"name": "Rene", "phonenumber":"+46700000000"},
    ]

    """

def get_active_user_name():
    try:
        with open("active_user.txt", "r") as f:
            return f.read().strip()
    except:
        return None

def set_active_user(username):
    with open("active_user.txt", "w") as f:
        f.write(username)


#
# Some helper functions to make the code below a bit more readable
#
def get_user_from_number(phonenumber):
    for user in get_users():
        if user['phonenumber'] == phonenumber:
            return user

def get_user_from_name(name):
    for user in get_users():
        if user['name'].lower() == name.lower():
            return user

def get_active_user():
    username = get_active_user_name()
    if username is not None:
        return get_user_from_name(username)


#
# Request handler for incoming SMS
#

@app.route('/incoming-sms', method='POST')
def incoming_sms():
    to_number = request.forms.get('to')
    from_number = request.forms.get('from')
    message = request.forms.get('message')

    # Verify that the SMS is from a trusted user
    user = get_user_from_number(from_number)

    if user is None:
        return "Hey, you are not allowed to be here"

    #
    # Set a new user as active
    # Send "set Martin" in a sms
    #
    if message.lower().startswith("set "):
        newUser = get_user_from_name(message[4:])
        if newUser is None:
            return f"No user with name '{message[4:]}' found"

        # Store the new active user
        set_active_user(newUser['name'])

        return f"Set {newUser['name']} as active, they will recieve incoming calls now"

    #
    # Ask the system which user is active
    #
    elif message.lower().startswith("who"):
        activeUser = get_active_user()
        if activeUser == None:
            return "No active user at the moment"
        else:
            return f"{activeUser['name']} is the active user"

    elif message.lower().startswith("disable"):
        set_active_user("")
        return f"Disabled the phone switch (removed the active user)"

    elif message.lower().startswith("help"):
        set_active_user("")
        return """Available commands:
Set [name] x- Set user [name] as active user
disable - Remove the active user
who - Responds with name of the active user"""


    return "Sorry, I don't understand that command"

#
# Request handler for incoming calls
#
@app.route('/incoming-call', method='POST')
def incoming_call():
    to_number = request.forms.get('to')
    from_number = request.forms.get('from')

    active_user = get_active_user()

    if active_user is not None:

        # Connect the call to the active user. If the connect failes
        # or the active user is already in a call, play a recording
        voice_start = {
            'connect': active_user['phonenumber'],
        }

    return json.dumps(voice_start)

run(app, host=config['host'], port=config['port'])
