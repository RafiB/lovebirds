#!/import/adams/1/rble114/lovebirds/bin/python

from __future__ import with_statement
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from ast import literal_eval
app = Flask(__name__)
app.config.from_object(__name__)

DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__, template_folder="../static/templates")
app.secret_key = SECRET_KEY
app.debug = DEBUG

@app.route('/')
def mainPage():
    return render_template('main.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)


"""
            <a href="javascript:toggleElement('how-to')"><img src="../static/LovebirdsPlus.gif" alt="http://www.water.ca.gov/wateruseefficiency/images/plus_sign.gif">How to use Lovebirds</a>
            <div id="how-to" style="display:none">
                Making a timetable with another person is the ultimate way to show
                love and devotion. However, if you've ever met me, you'd understand
                that I'm the type of person who'd eventually try to write code to
                deal with messy emotions for him, and.... you'd be correct!
                Lovebirds is an auto-timetabler that takes two people's subjects
                for the current semester and creates a set of timetables that put
                the people together in as many classes as possible.<p />
                Just enter your courses codes in the boxes, separated by spaces.
                For example, "COMP1917 MATH1141 PHYS1131 ENGG1000" for Person 1 and
                "COMP1927 MATH1141 MATH1081" for Person 2 - then Make love! and
                watch the magic happen!

            </div><p />

            <a href="javascript:toggleElement('FAQ')"><img src="../static/LovebirdsPlus.gif" alt="http://www.water.ca.gov/wateruseefficiency/images/plus_sign.gif">FAQ</a>
            <div id="FAQ" style="display:none">
                <ol>
                    <li>Do you have to be in love with another person to use Lovebirds?</li>
                    No - even though this program runs on the magic of love, this code will work for anyone, anywhere, until the day that all love on the planet dies.
                </ol>
            </div>

            <hr>
            By Rafi Blecher, heavily based on <a href="http://circles.epochfail.com">Circles</a> by Evgeny Martynov</p>
            <i>N.B. Due to the NP-complete nature of <a
            href="http://theconversation.com/timetables-hard-to-read-even-harder-to-build-1308">the
            Timetable Construction Problem</a>, this can be a little slow - if
            it's taking an inordinately long amount of time then either leave
            and come back to it another time, or contact me and I can see if
            there really is a problem.</i>
"""
