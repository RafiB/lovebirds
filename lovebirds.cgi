#!/usr/bin/python

#############################################
#             By Rafi Blecher               #
# Based heavily off code by Evgeny Martynov #
#############################################

import circles_interface

import cgi
import cgitb

import re

cgitb.enable()

# http://getbootstrap.com/2.3.2/assets/css/bootstrap.css
# http://getbootstrap.com/2.3.2/assets/css/bootstrap-responsive.css

def printTop():
    print """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>Lovebirds</title>
        <link rel="stylesheet" type="text/css" href="../static/bootstrap.css">
        <link rel="stylesheet" type="text/css" href="../static/bootstrap-responsive.css">
    </head>

    <script>
        function toggleElement(id) {
            if(document.getElementById(id).style.display == 'none') {
                document.getElementById(id).style.display = '';
            }
            else {
                document.getElementById(id).style.display = 'none';
            }
        }
    </script>

    <body>
        <div class="container">
            <div class="row">
                <H2>Lovebirds</H2>
                <img src="LovebirdsLogo.jpg" alt="http://3.bp.blogspot.com/_XdP6Lp2ceqY/TUbhoAwGYlI/AAAAAAAAlOc/do83f7IKpUs/s400/636x460design_01.jpg">
            </div>
            <div class="row">

            <!-- TODO: add functionality for n timetables -->
                <form action="lovebirds.cgi" method="post">
                    <label style="display:block" for="p1">Person
                    1</label><input id="p1" type="text" name="p1in"><input type="text" name="p1clash" placeholder="Clash hours (max 3)">
                    <label style="display:block" for="p2">Person 2</label><input id="p2" type="text" name="p2in"><input type="text" name="p2clash" placeholder="Clash hours (max 3)">
                    <input type="submit" value="Make love!" />
                </form>
            </div>
            """

def printBottom():
    print """
            <a href="javascript:toggleElement('how-to')"><img src="LovebirdsPlus.gif" alt="http://www.water.ca.gov/wateruseefficiency/images/plus_sign.gif">How to use Lovebirds</a>
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

            <a href="javascript:toggleElement('FAQ')"><img src="LovebirdsPlus.gif" alt="http://www.water.ca.gov/wateruseefficiency/images/plus_sign.gif">FAQ</a>
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
        <!--</div>-->
    </div>
    </body>

</html>"""

def printTimetables(p1in, p2in, P1_CLASHES, P2_CLASHES, timeout):
    SORTING_ORDER = None
    MAX_OPTIONS = 40 #int(options.num_timetables or 100)

    person1_subjects = []
    person2_subjects = []
    validCourses = 1
    valid = re.compile("[a-zA-Z]{4}[0-9]{4}")
    for item in p1in.split():
        if not valid.match(item):
            validCourses = 0
        else:
            person1_subjects.append(item.upper())
    for item in p2in.split():
        if not valid.match(item):
            validCourses = 0
        else:
            person2_subjects.append(item.upper())

    #print 'Fetching timetables for', map(lambda x: x.upper(), subjects)

    if validCourses:
 #       startTime = time.time()
        tables = circles_interface.process(set(person1_subjects), set(person2_subjects), P1_CLASHES, P2_CLASHES, SORTING_ORDER)
#        if time.time() > startTime + timeout:
#            print "<H3>Fetching timetables timed out - see note at in page footer. If you would like to try again, click <a href='lovebirds.cgi?timeout=180'>here</a>."

        if not isinstance(tables, tuple):
            print "<H3>Classes could not be found for %s - are you sure it runs this semester? If you are, please contact <a href='mailto:rafiblecher@gmail.com'>Rafi Blecher</a><p /></H3>" % tables

        else:
            i = 0
            lens = map(len, (tables[0], tables[1]))
            timeOkay = True
            while i <= MAX_OPTIONS and i < min(lens) and timeOkay:
                print '<div class="row">'
                print '<span class="span6">'
                circles_interface.print_timetable(tables[0][i/2])
                print '</span>'
                print '<span class="span6">'
                circles_interface.print_timetable(tables[1][i/2], col=False)
                i += 2
                print '</span>'
                print '</div>'

            if i > MAX_OPTIONS:
                print 'Reached %d options; not printing out any more.' % MAX_OPTIONS

print 'Content-type: text/html\n\n'

form = cgi.FieldStorage()

p1in = form.getvalue('p1in')
p2in = form.getvalue('p2in')

p1clash = form.getvalue('p1clash')
if p1clash:
    p1clash = int(p1clash)
else:
    p1clash = 0

p2clash = form.getvalue('p2clash')
if p2clash:
    p2clash = int(p2clash)
else:
    p2clash = 0

timeout = form.getvalue('timeout')
printTop()

if p1in and p2in:
    printTimetables(p1in, p2in, p1clash, p2clash, timeout or 60)

printBottom()
