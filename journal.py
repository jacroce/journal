from sys import exit
from getpass import getuser
from time import localtime, strftime
from re import search
import sqlite3
from datetime import date


name = getuser()
current_hour = int(strftime('%H', localtime()))
ds = str(date.today())
act = ''
event = ''
event_time = ''


def greeting():
        print("Hello %s, how are you?") % name
        mood = raw_input("> ")
        if search('[a-zA-Z]', mood) > 0:
            event_condition()
        else:
            if current_hour < 12:
                print("You clearly are not awake yet. Take a nap.")
                exit(0)
            else:
                print("I think you stayed up a little too late. Go to sleep.")
            exit(0)


def event_condition():
    if current_hour < 12:
        goals()
    else:
        completion()


def goals():
        global act
        global event
        print """
        Glad to hear it.

        What would you like to do today?
        Your options are:
        1. Work
        2. Gym
        3. Read
        4. Code
        5. Models
        6. Music
        """

        event = 'aspire'
        act = raw_input("> ")
        if act in (['Work', 'Gym', 'Read', 'Code', 'Models', 'Music']):
            if current_hour < 12:
                hours_aspired()
            else:
                hours_spent()
        else:
            print 'failed'


def completion():
        global act
        global event
        print """
        Glad to hear it.

        What did you set out to do today?
        Your options are:
        1. Work
        2. Gym
        3. Read
        4. Code
        5. Models
        6. Music
        """

        event = 'completed'
        act = raw_input("> ")
        if act in (['Work', 'Gym', 'Read', 'Code', 'Models', 'Music']):
            hours_spent()
        else:
            print 'failed'


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def hours_aspired():
        global event_time
        print """
        Thank you!

        How many hours do you plan to spend on %s?
        """ % act

        event_time = raw_input("> ")
        if is_number(event_time) is True:
            db_enter()
        else:
            print 'Time is meaningless.'
        exit(0)


def hours_spent():
        global event_time
        print """
        Thank you!

        How many hours did you spend on %s?
        """ % act

        event_time = raw_input("> ")
        if is_number(event_time) is True:
            db_enter()
        else:
            print 'Time is meaningless.'
        exit(0)


def db_enter():
    conn = sqlite3.connect('journal.db', timeout=11)

    c = conn.cursor()

    c.execute('''INSERT INTO journal VALUES (?, ?, ?, ?)''',
              (ds, act, event, event_time))
    conn.commit()
    conn.close()
    print 'Thank you!'
    exit(0)


greeting()
