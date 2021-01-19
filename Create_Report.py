from Database import fetchspecificLocations, fetchbetweendates
from datetime import datetime, date, timedelta
import pygal
from collections import OrderedDict
import math

class array_circ(object):
    def __init__(self,data,pointer):
        self.data = data
        self.pointer = pointer
        self.slicelst_indexes = []
    
    def __str__(self):
        return self.data
    
    def current(self):
        return self.data[self.pointer]
    
    def __movepointerup(self):
        if self.pointer == len(self.data) - 1:
            self.pointer == 0
        else:
            self.pointer += 1

    def __movepointerdown(self):
        if self.pointer == 0:
            self.pointer = len(self.data) - 1
        else:
            self.pointer -= 1

    def get_to(self,index):  # index the amount away from current position
        slicelst = []
        slicelst_indexes = []
        slicelst.append(self.data[self.pointer])  # i want it to include the current month
        slicelst_indexes.append(self.pointer + 1)
        if index > 0:
            for i in range(abs(index)):
                self.__movepointerup()
                slicelst.append(self.data[self.pointer])
                slicelst_indexes.append(self.pointer + 1)
        elif index < 0:
            for i in range(abs(index)):
                self.__movepointerdown()
                slicelst.append(self.data[self.pointer])
                slicelst_indexes.append(self.pointer + 1)
        else:
            return slicelst
        self.currentsliceindexes = slicelst_indexes
        return slicelst
    
    def get_to_asint(self):
        return self.currentsliceindexes
    
    # will make another function to get between two values, or set pointer to somewhere then getto
            
class siteAnalysis(object):  # right now this only works with reports starting from today, i should support other times too
    def __init__(self,siteinfo,datefrom,entries,reporttype):  # latest, oldest ?
        self.entries = entries
        self.reporttype = reporttype
        self.datefrom = datefrom
        self.dateto = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        self.months = array_circ(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],(datetime.today().month - 1))
        self.sitename = siteinfo[1]
        self.amtplasticbin = siteinfo[2]
        self.amtpaperbin = siteinfo[3]
        self.amtglassbin = siteinfo[4]

        #self.latestplastic = latest[0]  # these were for potentially showing the start --> end values
        #self.latestpaper = latest[1]
        #self.latestglass = latest[2]

        #self.oldestplastic = oldest[0]
        #self.oldestpaper = oldest[1]
        #self.oldestglass = oldest[2]
    
        self.generatexvalues()
        self.generategraphpng(entries,'dummypath')

        # maybe have an overall site usage - e.g calculate the mean usage over time
        # and mean usage total over the time period
        # bubble chart at end of report showing most and least used sites 'means'

    def gettitle(self):
        return self.sitename

    def generategraphpng(self,data,path):  # path to save
        self.usage_chart = pygal.DateLine(x_label_rotation=25)
        self.usage_chart.title = 'Usage over time for ' + self.sitename
        self.usage_chart.y_labels = list(i for i in range(0, 110,10))  # 10 is the step
        self.usage_chart.x_labels = self.x_values
        self.usage_chart.show_x_guides = True  # show grid lines for both axis
        self.usage_chart.show_y_guides = True
        self.usage_chart.__init__

        print(self.entries)

        Plastic = [(entry[0],entry[2]) for entry in self.entries]
        Paper = [(entry[0],entry[3]) for entry in self.entries]
        Glass = [(entry[0],entry[4]) for entry in self.entries]

        self.usage_chart.add("Plastic",Plastic)
        self.usage_chart.add("Paper",Paper)
        self.usage_chart.add("Glass",Glass)

        self.usage_chart.render_to_png((self.sitename).replace(' ','_') + '.png')
    
    def months_since(self,target):  # can make this months between when needed
        num_months = (self.dateto.year - target.year) * 12 + (self.dateto.month - target.month)
        return num_months

    def generatexvalues(self):  # maybe this should be done outside the function if they are all for same time
        # because currently it is repeated for each site which is unecessary
        # maybe put it in an init of a report class when it is made
        months_since = self.months_since(self.datefrom)
        self.x_values = ()  # a tuple
        labels = []
        years = []

        if months_since == 0:
            self.checkweeklymonthly()
        else:
            monthlist = self.months.get_to((0 - months_since))
            int_months = self.months.get_to_asint()
            
            year = self.dateto.year
            for i in range(len(monthlist)):  # adds the correct year to each month
                labels.append(monthlist[i] + ' ' + str(year))
                years.append(year)
                if i != len(monthlist) - 1:
                    if monthlist[i] == 'Jan' and monthlist[i + 1] == 'Dec':
                        year -= 1
            
            values = list(map(lambda x,y: date(x,y,1),years,int_months))

            for i in range(len(labels)):
                tempdict = {}
                tempdict['label'] = labels[i]
                tempdict['value'] = values[i]
                self.x_values = self.x_values + (tempdict, )

    def checkweeklymonthly(self):
        pass
        
    def generatemeandata(self,label,data):
        pass  # find means of all the data entries

    def findtotalmean(self):
        pass  # find the mean

def callAnalysis(datefrom,sitestoinclude):  # sitestoinclude has to be a tuple, and in alphabetical order
    sitestoinclude = tuple(sitestoinclude)
    locationdata = fetchspecificLocations("Localhost", sitestoinclude)
    sitedata = fetchbetweendates("Localhost",datefrom,sitestoinclude)  # filtering out locations where no data is found

    namesonly = [site[1] for site in sitedata]  # site 1 is the name
    sitesincluded = list(OrderedDict.fromkeys(namesonly))  # dictionaries cant have any duplicates so useful here
    locationdata_filtd = [i for i in locationdata if i[1] in sitesincluded]

    sitedata_split = sublists(sitesincluded,sitedata,namesonly)  #
    
    graphobjects = []
    for i in range(len(sitesincluded)):
        graphobjects.append(siteAnalysis(locationdata_filtd[i],datefrom,sitedata_split[i],'yearly'))
    

def sublists(lookfor,lst,namesonly):  # sitedata has been alphabetically ordered by name
    newlist = []
    startpos = 0
    if len(lookfor) > 1:
        for i in range(len(lookfor) - 1):
            endpos = namesonly.index(lookfor[i + 1])
            newlist.append(lst[startpos:endpos])
            startpos = endpos
    endpos = len(lst)
    newlist.append(lst[startpos:endpos])
    return newlist
    
#when using this on another computer, need to find the path of the current file name to save there
#callAnalysis(datetime.today().replace(day=1,month=1,hour=0, minute=0, second=0, microsecond=0),['Asda Ellis Way','Beeston Street','Pier','Boating lake'])
callAnalysis(date(2020,11,1),['Asda Ellis Way','Beeston Street','Pier','Boating lake'])  # maybe i can make an advanced customisability at some point
# slightly problematically, pygal uses utc time by default -- might not cause any issues still

# have a 'this month feature', 'past 30 days feature'
# search the lists using re, regular expression
# sites to include must be alpha

#def generatereportpath(self,reporttype):    #  i think this would go into the report class
#today = (str((datetime.today()))[:-7]).replace(' ','_')
#filename = 'report' + '-' + date + '.pdf'
#path = '/home/livi/NEA/Past_Reports/' + filename
