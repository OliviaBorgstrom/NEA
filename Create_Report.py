from Database import fetchspecificLocations, fetchbetweendates
from datetime import datetime, date, timedelta
import pygal
from collections import OrderedDict

class siteAnalysis(object):
    def __init__(self,siteinfo,latest,oldest,datefrom):
        self.sitename = siteinfo[0]
        self.amtplasticbin = siteinfo[1]
        self.amtpaperbin = siteinfo[2]
        self.amtglassbin = siteinfo[3]
       
        self.latestplastic = latest[0]
        self.latestpaper = latest[1]
        self.latestglass = latest[2]

        self.oldestplastic = oldest[0]
        self.oldestpaper = oldest[1]
        self.oldestglass = oldest[2]
    
        self.initTimes()

        # maybe have an overall site usage - e.g calculate the mean usage over time
        # and mean usage total over the time period
    
    def initTimes(self):
        self.thismonth = datetime.today().replace(day=1,hour=0, minute=0, second=0, microsecond=0)
        self.thisyear = datetime.today().replace(day=1,month=1,hour=0, minute=0, second=0, microsecond=0)
        self.sevendaysago = (datetime.today() - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        self.past12months = (datetime.today() - timedelta(months=12)).replace(day=1,hour=0, minute=0, second=0, microsecond=0)
        self.past30days = (datetime.today() - timedelta(days=30)).replace(day=1,hour=0, minute=0, second=0, microsecond=0)
        
        print(self.thismonth,self.thisyear,self.sevendaysago,self.past12months,self.past30days)

    def generatereportpath(self,reporttype):
        today = (str((datetime.today()))[:-7]).replace(' ','_')
        filename = 'report' + '-' + date + '.pdf'
        path = '/home/livi/NEA/Past_Reports/' + filename
        
    def generategraphpng(self,data,path):  # path to save
        self.usage_chart = pygal.DateLine(x_label_rotation=25)
        self.usage_chart.title = 'Usage over time for ' + self.sitename
        self.usage_chart.y_labels = list(i for i in range(0, 110,10))  # 10 is the step
        self.usage_chart.show_x_guides = True  # show grid lines for both axis
        self.usage_chart.show_y_guides = True
    
    def generatexvalues(self,datefrom):
        
        pass

    def generatemeandata(self,label,data):
        pass  # find means of all the data entries

    def findtotalmean(self):
        pass  # find the mean

def callAnalysis(datefrom,sitestoinclude):  # sitestoinclude has to be a tuple, and in alphabetical order
    sitestoinclude = tuple(sitestoinclude)
    locationdata = fetchspecificLocations("Localhost", sitestoinclude)
    sitedata = fetchbetweendates("Localhost",datefrom,sitestoinclude)
    
    namesonly = [site[1] for site in sitedata]  # site 1 is the name
    sitesincluded = list(OrderedDict.fromkeys(namesonly))  # dictionaries cant have any duplicates so useful here
    sitedata_split = sublists(sitesincluded,sitedata,namesonly)  #
    
    print(sitedata_split)
    #graphobj1 = siteAnalysis(locationdata)
    #mapobj = list(list(map(Filter,sitestoinclude,sitedata)))

def sublists(lookfor,lst,namesonly):  # sitedata has been alphabetically ordered by name
    newlist = []
    startpos = 0
    if len(lookfor) > 1:
        for i in range(len(lookfor) - 1):
            print(lookfor[i])
            endpos = namesonly.index(lookfor[i + 1])
            print(endpos)
            newlist.append(lst[startpos:endpos])
            startpos = endpos
    print(lst)
    endpos = len(lst)
    print(startpos,endpos)
    newlist.append(lst[startpos:endpos])
    return newlist
    
#when using this on another computer, need to find the path of the current file name to save there

print(datetime.today().replace(day=1,month=1,hour=0, minute=0, second=0, microsecond=0))
callAnalysis(datetime.today().replace(day=1,month=1,hour=0, minute=0, second=0, microsecond=0),['Asda Ellis Way','Beeston Street','Pier','Boating lake'])

#print(datetime.today - 2)
# slightly problematically, pygal uses utc time by default -- might not cause any issues still

# have a 'this month feature', 'past 30 days feature'
# search the lists using re, regular expression
# sites to include must be alpha
