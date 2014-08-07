#!/usr/bin/python

#############################################
#             By Rafi Blecher               #
# Based heavily off code by Evgeny Martynov #
#############################################

import sys

import circles_generator, circles_interface

import cgi
import cgitb

import re

cgitb.enable()

print 'Content-type: text/html\n\n'

print """<html>
    <head>
        <title>Response</title>
    </head>

    <body>"""

form = cgi.FieldStorage()

p1in = form.getvalue('p1in')
p2in = form.getvalue('p2in')

SORTING_ORDER = None
MAX_OPTIONS = 40 #int(options.num_timetables or 100)
P1_CLASHES = 0 #min(int(options.clash_hours_1 or 0), 3)
P2_CLASHES = 0 #min(int(options.clash_hours_2 or 0), 3)

person1_subjects = []
person2_subjects = []
valid = 1
valid = re.compile("[a-zA-Z]{4}[0-9]{4}")
for item in p1in.split():
    if not valid.match(item):
        valid = 0
    else:
        person1_subjects.append(item)
for item in p2in.split():
    if not valid.match(item):
        valid = 0
    else:
        person2_subjects.append(item)

    #print 'Fetching timetables for', map(lambda x: x.upper(), subjects)

if valid:
    tables = circles_interface.process(set(person1_subjects), set(person2_subjects),
                                   SORTING_ORDER, P1_CLASHES, P2_CLASHES)

    i = 0
    failed = 0
    while i <= MAX_OPTIONS and failed < 2:
        failed = 0
        try:
            print "Person 1:"
            circles_interface.print_timetable(tables[0][i/2])
        except IndexError:
            failed += 1
        try:
            print "Person 2:"
            circles_interface.print_timetable(tables[1][i/2])
        except IndexError:
            failed += 1
        i += 2
    if i > MAX_OPTIONS:
        print 'Reached %d options; not printing out any more.' % MAX_OPTIONS

    print 'Got %d timetable options!' % (i / 2)

print """   </body>
</html>"""
