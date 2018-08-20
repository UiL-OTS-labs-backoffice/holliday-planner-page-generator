#!/usr/bin/env python3
import datetime, sys
import argparse

class holliday_planner(object):

    COLORS = ['green', 'red', 'purple', 'magenta', 'orange', 'blue', 'cyan',
              'violet', 'yellow', 'wheat']
    DAYS   = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
              "Sunday"]
    MONTHS = ["January", "February", "March", "April", "May", "June",
              "July" , "August", "September", "October",
              "November", "December"]

    def __init__(self, year, names):
        '''
        Generate a calendar for this year
        '''
        self.away = dict()
        self.header = [
            '[[Category:HolidayRoster]]', 
            '', 
            ( 'You can find how to correctly edit this page on in'
              '[[:Category:HolidayRoster | the category page]].'), 
            '==Holidays=='
        ]
        self.namesHeader = [
            '',
            '==How to add to the table==',
            'To add your own name, just find the correct cell.',
            'Add your own name, with a nice color by by using HTML.',
            '<syntaxhighlight lang="html4strict">',
            '<br/> <font color="<yourColor>"> <yourname> </font>',
            '</syntaxhighlight>',
            '',
            '==List of names and colors==',
            'The following is a list of all names that have been used already'
        ]
        self.names = sorted(names)
        self.DELTA = datetime.timedelta(1)
        self.SKIP_WEEKEND = datetime.timedelta(2)
        self.year = year
        self.getColorNames()

    def getColorNames(self):
        self.colorNames = dict(
            (self.names[i], self.COLORS[i]) for i in range(len(self.names))
            )

    def addName(self, name, date):
        '''
        Puts a name on unavailable
        Date in datetime.date format
        '''
        try:
            self.away[date] += '\n<br><font color="%s">%s</font>' % (self.colorNames[name], name)
        except:
            self.away[date] = '\n<br><font color="%s">%s</font>' % (self.colorNames[name], name)

    def addNameLong(self, name, begin, end):
        '''
        Adds a name to unavailable for a series of dates
        Name is a string, begin and end in datetime.date format
        '''
        assert begin < end
        while begin <= end:
            self.addName(name, begin)
            begin += self.DELTA

    def datetext(self, date):
        '''formats the text that indicates the date nicely'''
        return "<font size=\"0.8\">%d %s</font>" %(date.day, self.MONTHS[date.month - 1])

    def generateCalendar(self):
        '''generates the calendar'''
        d = datetime.date(self.year, 1, 1)
        lst = ['{| class="wikitable"\n|-\n! Monday !! Tuesday !! Wednesday !! Thursday !! Friday\n|-\n']
        lst += ["| " + " || ".join([self.datetext(d - datetime.timedelta(i+1)) for i in range(d.weekday())][::-1])]
        while d < datetime.date(self.year + 1, 1, 1):
            lst += ["%s %s " % ("\n\n|| " if d.weekday() > 0 else "", self.datetext(d))]
            if d in self.away:
                lst+= [self.away[d]]
            d += self.DELTA
            if d.weekday() > 4:
                d += self.SKIP_WEEKEND
                lst += ["\n|-\n|"]
        lst += ["||" if d.weekday() > 0 else "" + " || ".join([self.datetext(d + datetime.timedelta(i-d.weekday())) for i in range(d.weekday(), 5)])]
        lst += ["\n|}"]
        return lst

    def createPlanner(self):
        '''writes the calendar'''
        with open("calendar.txt", 'w') as stream:
            for h in self.header:
                stream.write(h)
                stream.write("\n")
            self.writeCalendarTable(stream)
            for nh in self.namesHeader:
                stream.write(nh + "\n")
            self.writeNamesTable(stream)

    def writeCalendarTable(self, stream):
        for r in self.generateCalendar():
            stream.write(r)

    def writeNamesTable(self, stream):
        stream.write('\n\n\n{| class="wikitable"\n|-\n! Name !! Color !! HTML Line\n|-\n')
        for k in sorted(self.colorNames.keys()):
            stream.write('|<font color=' + self.colorNames[k] + '>' + k + '</font> || ' + self.colorNames[k] + '|| <syntaxhighlight lang="html4strict"><br /><font color=' + self.colorNames[k] + '>' + k + '</font></syntaxhighlight>\n|-\n')
        stream.write("|}")


DESCRIPTION = ('holidayplanner is a utility to write the wikitable necessary '
               'to update the holiday schedule for one year. The user is '
               'expected to provide the names necessary to put in the page.'
               'It is also recommended to use the --year or -y option to '
               'generate the list for the intended year, otherwise the current '
               'year + 1 is chosen.')
ARGPARSER = argparse.ArgumentParser(description=DESCRIPTION)
ARGPARSER.add_argument("names",
                        help=(r'Names to store inside the generated pages '
                              r'Example: "Maarten Duijndam" "Iris Mulders"'),
                        nargs='+',
                        type=str
                        )
ARGPARSER.add_argument("-y",
                       "--year",
                       type=int,
                       default=datetime.date.today().year + 1,
                       help='The year to use to generate the calendar'
                       )
ARGPARSER.add_argument("-s",
                       "--silent",
                       action='store_true',
                       help='Reduce the output of the holiday planner.'
                       )

if __name__ == '__main__':
    arguments   = ARGPARSER.parse_args()
    year        = arguments.year
    names       = arguments.names
    calendarfn  = 'rawcalendar.txt' 
    namesfn     = 'names.txt'

    cal = holliday_planner(year, names)

    # Example for how to add predefined hollidays
    # cal.addNameLong("Maarten Duijndam", datetime.date(year, 7, 10), datetime.date(year, 8, 19))
    # cal.addNameLong("Iris Mulders", datetime.date(year, 7, 14), datetime.date(year, 8, 6))
    # cal.addNameLong("Iris Mulders", datetime.date(year, 8, 25), datetime.date(year,8,31))
    # cal.addName("Jan de Mooij", datetime.date(year, 6, 16))
    # cal.addNameLong("Jan de Mooij", datetime.date(year, 7, 27), datetime.date(year, 8, 4))

    cal.createPlanner()
    with open(calendarfn, 'w') as stream: 
        cal.writeCalendarTable(stream)
        if not arguments.silent:
            print("Written the holiday wikitable to {}".format(calendarfn))
    with open(namesfn, 'w') as stream:
        cal.writeNamesTable(stream)
        if not arguments.silent:
            print("Written the names legend to {}".format(namesfn))
