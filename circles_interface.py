#############################################
#             By Rafi Blecher               #
# Based heavily off code by Evgeny Martynov #
#############################################

import re, urllib, os
from datetime import datetime, timedelta, date
import circles_generator

from tempfile import mkstemp
from subprocess import Popen as popen, PIPE

URL_BASE = r'http://www.timetable.unsw.edu.au/'+str(date.today().year)+'/%s.html'
OFFSET = 6
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
tags_re = re.compile(r'<[^>]*>')
dow_re = re.compile(r'\([^\(]*\)')

class CirclesError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

def print_timetable(times, col=True):
    days = len(times)
    slots = len(times[0])

    blockSizes = []

    for d in xrange(5):
        blocks = []
        time = times[d][9:22] + [1]
        lastSeen = time[0]
        seen = 0
        for t in time:
            if t == lastSeen:
                seen += 1
            else:
                blocks.append((seen, lastSeen))
                seen = 1
                lastSeen = t
        blockSizes.append(blocks)

    blockSizes = map(list, map(None, *blockSizes))
    grid = createTimeTableGrid(times)
    
    table = ""

    table += "                <table  style='min-height:700px;' class='table table-bordered table-condensed'>\n"
    table += "                    <tr>\n"

    table += "                        <td class='short'></td>\n"
    for d in xrange(days):
        table += "                        <td>%s</td>\n" % DAYS[d]
    table += "                    </tr>\n"

    blockSizesIndex =    [-1, -1, -1, -1, -1] 
    blockSizesLastSeen = ["", "", "", "", ""]
    for hour in xrange(13): # 12 hour day, 0900 - 2100
        table += "                    <tr>\n"
        if col:
            table += "                        <td class='short'>%s</td>\n" % (hour + 9)
        else:
            table += "                        <td class='short'><font color='white'>%s</font></td>\n" % (hour + 9)
        for day in xrange(len(grid[hour])): # should be 5 .... right?
            currClass = grid[hour][day]
            #print currClass
            #print day, hour + 9

            if day < len(blockSizesIndex): # and day < len(blockSizes):
                if blockSizesIndex[day] + 1 < len(blockSizes): # we're going to add one before we use it
                    if currClass != blockSizesLastSeen[day]:
                        blockSizesIndex[day] += 1
                        blockSizesLastSeen[day] = grid[hour][day]
                        blockSizeInfo = blockSizes[blockSizesIndex[day]][day]
                        style = "style='background-color:#E1FFE3'" if blockSizeInfo[1] else "style='background-color:#FFEDE1'"
                        #style = ''
                        table += "                        <td class='span2' rowspan='%s'%s>%s</td>\n" %(blockSizeInfo[0], style, blockSizeInfo[1] or "")
                    
        table += "                    </tr>\n"

    table += "                 </table>\n"

    print table

def createTimeTableGrid(times):
    return map(list, zip(*times))[9:22]

html_page_cache = {}
def get_classes(subject):
    def fetch_html():
        url = URL_BASE % subject
        return urllib.urlopen(url)

    def fetch_classes():
        lines = map(lambda x: x.strip(), [line for line in fetch_html()])
        classes = {}

        i = 0
        while i < len(lines)-5:
            sem = "1"
            if date.today().month >= 6:
                sem = "2"
            if '#S'+sem+'-' in lines[i]:
                name = subject + ' ' + re.sub(tags_re, '', lines[i], 10)

                times_line    = ''
                abort_counter = 0
                while '</td>' not in times_line:
                    # TODO: make this less idiotic
                    if abort_counter > 15:
                        raise CirclesError('Detected runaway parser while processing subject %s. Contact Evgeny to fix.' % subject)
                    times_line += lines[i+OFFSET+abort_counter] + '\n'
                    abort_counter += 1

                times = re.sub(tags_re, '', times_line, 10)
                # Readability? Fuck that.
                times = [(dow_to_int(time[0]), int(time[1][:2]), int(time[3][:2])) for time in filter(bool, map(str.split, map(str.strip, re.sub(dow_re, '', times).split(', '))))]
                times = list(set(times))
                if times:
                    classes[name] = classes.get(name, []) + [times]
                i += OFFSET
            else:
                i += 1

        return classes

    def expired():
        if subject not in html_page_cache:
            return True

        timediff = datetime.now() - html_page_cache[subject][0]
        return timediff > timedelta(hours=1)

    def update():
        html_page_cache[subject] = (datetime.now(), fetch_classes())

    def get():
        return html_page_cache[subject][1]

    if (expired()):
        update()

    results = get()
#    if not results:
#        raise CirclesError('Could not find subject `%s\' or it has no times listed. Try removing it or check the spelling.' % subject)
    return results

"""
def process_v2(subjects, SORTING_ORDER=None, CLASHES=0, NUM_RESULTS=0):
    def make_subject_file():
        data = map(get_classes, subjects)

        fd, fname = mkstemp(suffix='.crcl')
        def pr(*args):
            os.write(fd, ' '.join(map(unicode, args)) + '\n')

        pr(len(subjects), 13)

        for di in xrange(len(data)):
            pr('%s' % subjects[di])
            d = data[di]

            classes = []

            for k,v in d.iteritems():
                nm = k.split(' ', 1)[1]
                for t in v:
                    classes.append((nm, t))

            pr('  %d' % len(classes))
            for c in classes:
                pr('    %s' % c[0])
                pr('      %d' % len(c[1]))
                for t in c[1]:
                    dow = DAYS[t[0]]
                    pr('        %s %d-%d' % (dow, t[1], t[2]))

        os.close(fd)
        return fname

    fname = make_subject_file()
    args = ['circles-generator', fname, SORTING_ORDER, str(NUM_RESULTS), str(CLASHES)]
    stream = popen(args, stdout=PIPE)

    num_tables = int(stream.stdout.readline())
    data = stream.stdout.readline()

    os.unlink(fname)

    return num_tables, json.loads(data)
"""

def print_classes(classes):
    for k, v in classes.iteritems():
        print '%s\n\t%s\n' % (k, '\n\t'.join(map(str, v)))

def dow_to_int(s):
    return DAYS.index(s)

def process(p1Subjects, p2Subjects, P1_CLASHES, P2_CLASHES, SORTING_ORDER=None):
    shared_classes = {}

    p1_classes = {}
    p2_classes = {}

    sharedSubjects = set.intersection(p1Subjects, p2Subjects)
    p1Subjects = set.difference(p1Subjects, sharedSubjects)
    p2Subjects = set.difference(p2Subjects, sharedSubjects)

    for classTup in [ (p1Subjects, p1_classes),
                      (p2Subjects, p2_classes),
                      (sharedSubjects, shared_classes) ]:
        for c in classTup[0]:
            classes = get_classes(c)
            classTup[1].update(classes)
#            if not classes:
#                pass

     #           return c

    stuff = shared_classes.items()
    time_slots = [[False] * 24 for i in xrange(5)]
    tables = circles_generator.generate(stuff, time_slots, 0)
    # CLASHES is 0... if you try for clashes in your shared classes, you're
    # gonna have a bad time.

    tables.sort()

#    p1_tables = None
#    p2_tables = None

    for t in tables:
        p1_tmp_tables = tryMatch(t, p1_classes, P1_CLASHES)
        if p1_tmp_tables is not None:
            p2_tmp_tables = tryMatch(t, p2_classes, P2_CLASHES)
            if p2_tmp_tables is not None:
                p1_tables = p1_tmp_tables
                p2_tables = p2_tmp_tables

    p1_tables = circles_generator.sort_timetables(p1_tables, SORTING_ORDER)
    p2_tables = circles_generator.sort_timetables(p2_tables, SORTING_ORDER)

    return (p1_tables, p2_tables)

def tryMatch(base, additive, CLASHES):
    tables = circles_generator.generate(additive.items(), base, CLASHES)

    if tables == []:
        return None

    tables.sort()

    uniq = []
    for t in tables:
        if uniq == [] or uniq[-1] != t:
            uniq.append(t)

    return uniq
