from sorting_alg import quicksort
from Database import fetchspecificLocations, fetchbetweendates
from datetime import datetime, date, timedelta
import pygal
from collections import OrderedDict
import math
import numpy as np
from functools import reduce
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pygal.style import Style,CleanStyle
import os

class Report(object):  # this init is way too long
    def __init__(self,iscomparing,dateto,datefrom,filteredlocations,sitestoinclude,host):
        self.iscomparing = iscomparing[0]
        self.dataObjects = []
        self.datefrom = datefrom
        self.dateto = dateto
        self.sitestoinclude = sitestoinclude
        self.filteredlocations = filteredlocations
        self.host = host
        self.anydata = True  # assume there is data by default
        self.generatereportpath()

        self.title = 'An Analysis of Bring To Site Usage Between ' + str(datefrom) + ' and ' + str(dateto)
        self.template_vars = {}
        self.template_vars['title'] = self.title

        self.y_values = list(i for i in range(0, 110,10))
        self.num_months = (self.dateto.year - self.datefrom.year) * 12 + (self.dateto.month - self.datefrom.month)
        if self.num_months == 0:
            self.num_days = self.dateto.day - self.datefrom.day
            if self.num_days <= 7:
                #self.generatex_values_weekly()
                self.x_values = 'not needed'
                self.initAnalysisObj(weeklyAnalysis)
                self.getAnalysisTemplate_vars()
                self.renderhtml("html_templates/weeklyReport.html")
                self.reportTitle = '(weekly)' + self.reportTitle
            else:
                #self.generatex_values_monthly()
                #self.initAnalysisObj(monthlyAnalysis)
                self.initAnalysisObj(Analysis)
                self.getAnalysisTemplate_vars()
                self.generateOverallSummary()
                self.renderhtml("html_templates/mainReport.html")
        else:
            self.generatex_values()
            self.initAnalysisObj(Analysis)
            self.getAnalysisTemplate_vars()
            self.generateOverallSummary()
            self.renderhtml("html_templates/mainReport.html")
        
        if iscomparing[0]:
            comparepath = 'Past_html/' + iscomparing[1] + '.html'
            self.compareReports(comparepath)

    def initAnalysisObj(self, AnalysisClass):  # can add a thing at the bottom saying -> no data found for ...
        self.sitestoinclude = tuple(self.sitestoinclude)
        sitedata = fetchbetweendates('desktop','password',self.host,self.datefrom,self.dateto,self.sitestoinclude)  # filtering out locations where no data is found
        available_sites = [site[1] for site in sitedata]  # site 1 is the name
        self.sitesincluded = list(OrderedDict.fromkeys(available_sites))  # dictionaries cant have any duplicates so useful here
        if len(self.sitesincluded) == 0:
            self.anydata = False
        else:
            sitedata_split = self.sublists(self.sitesincluded,sitedata,available_sites)
            for i in range(len(self.sitesincluded)):
                indexofsite = self.sitestoinclude.index(self.sitesincluded[i])
                self.dataObjects.append(AnalysisClass(self.x_values, self.y_values, self.filteredlocations[indexofsite],sitedata_split[i]))
        
    def getAnalysisTemplate_vars(self):
        #sitevars = [[each.totalMean,each.numPaper,each.numPlastic,each.numGlass,each.avr_paper_usage,each.avr_plastic_usage,each.avr_glass_usage] for each in self.dataObjects]
        #sites = [[self.dataObjects[i].sitename,self.dataObjects[i].usage_pngtitle,self.dataObjects[i].mean_pngtitle,sitevars[i]] for i in range(len(self.dataObjects))]
        sites = [each.getSiteProfile() for each in self.dataObjects]
        totalMeans = [each.totalMean for each in self.dataObjects]
        maxID = np.argmax(totalMeans)
        minID = np.argmin(totalMeans)
        self.template_vars['mostUsed'] = [sites[maxID][0], totalMeans[maxID]]
        self.template_vars['leastUsed'] = [sites[minID][0], totalMeans[minID]]
        self.template_vars['ListOfSites'] = self.sitesincluded
        self.template_vars['sites'] = sites
        
    def sublists(self,lookfor,lst,namesonly):  # sitedata has been alphabetically ordered by name
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
    
    def generatex_values(self):
        self.months = array_circ(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],(self.dateto.month - 1))
        self.x_values = ()  # a tuple
        labels = []
        years = []

        if self.num_months == 0:
            return
        else:
            monthlist = self.months.get_to((0 - self.num_months))
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
    
    def generateOverallSummary(self):
        line_chart = pygal.HorizontalBar()
        line_chart.y_labels = self.y_values
        line_chart.x_labels = [each.sitename for each in self.dataObjects]
        
        allplastic = [each.avr_plastic_usage for each in self.dataObjects]
        allpaper = [each.avr_paper_usage for each in self.dataObjects]
        allglass = [each.avr_glass_usage for each in self.dataObjects]
        line_chart.add('Plastic',allplastic)
        line_chart.add('Paper',allpaper)
        line_chart.add('Glass',allglass)
        line_chart.show_x_guides = True
        line_chart.show_y_guides = True
        line_chart.__init__
        line_chart.render_to_png('temp/Overallbarchart.png')
        self.template_vars['barchart'] = 'temp/Overallbarchart.png'
        
    def generatereportpath(self):
        self.reportTitle = str(self.datefrom) + '_to_' + str(self.dateto)
        self.reportPath = 'Past_Reports/' + self.reportTitle + '.pdf'  # add a number depending on if there is another or not
    
    def renderhtml(self,templatepath):
        if not self.anydata:
            print('no data found')
        else:
            env = Environment(loader=FileSystemLoader('.'))
            self.template = env.get_template(templatepath)
            html_out = self.template.render(self.template_vars)
            self.writeTofile(html_out)
            HTML(string=html_out,base_url=__file__).write_pdf(self.reportPath,stylesheets=["html_templates/style.css"])
            self.clearTemp()
    
    def compareReports(self,path):  # remember number of bins could change between the two
        sitesincluded = ['Boating Lake','Beeston Street','Asda Ellis Way']
        with open('Past_html/2020-11-01_to_2021-02-01.html') as fh:
            first_line = fh.readline()
            sitesInComparison = ((first_line[5:-5]).replace(', ',',')).replace('\'','')
            sitesInComparison = sitesInComparison.split(',')
            
            includeset = set(sitesincluded)  # using sets to find the intersection and see if empty
            compareset = set(sitesInComparison)
            intsect = includeset.intersection(compareset)
    
            if not intsect:  # an empty set is intepreted as false
                self.comparing = False  # return a helpful message
                print('none in common')
                return

        summary_boxes = self.extractSummaryBoxes(intsect)

    def extractSummaryBoxes(self,wanted):
        ''' this algorithm goes till the start reading tag then breaks so that the
        next for loop can continue from the line that the last one left off at
        so as to not unnecessarily loop through too many lines'''
        arr_summary_box = []
        i = 0  # keeps track of which secondary list you are in
        with open('Past_html/2020-11-01_to_2021-02-01.html') as fh:
            for line in fh:
                if line.strip() == '<!--_StartReading_-->':
                    break
            for line in fh:  # This keeps reading the file
                if line.strip() == '<!--_StopReading_-->':
                    break
                if line[:6] == '<!--S_':
                    site = (line[6:].replace('-->','')).rstrip('\n')
                    if site in wanted:
                        arr_summary_box.append([site])
                        for line in fh:
                            if line.strip() == '<div class=\"summary_box\" style=\"width:450px\">':
                                break
                        for line in fh:
                            if line.strip() == '</div>':
                                break
                            arr_summary_box[i].append(line.strip())
                        i += 1
        print(arr_summary_box)
        return arr_summary_box

    def writeTofile(self,html):
        htmlpath = 'Past_html/' + self.reportTitle + '.html'
        f = open(htmlpath, 'w')
        f.write(html)
        f.close()

    def clearTemp(self):
        for filename in os.listdir('temp'):
            filepath = 'temp/' + filename
            os.remove(filepath)

class Analysis(object):  # those which arent specifically monthly or weekly are just Analysis
    def __init__(self, x_values, y_values, siteInfo, entries):
        self.x_values = x_values
        self.y_values = y_values
        self.sitename = siteInfo[1]
        self.numPlastic = siteInfo[2]
        self.numPaper = siteInfo[3]  # number of bins of each type
        self.numGlass = siteInfo[4]
        self.entries = entries
        self.custom_style = Style(
            title_font_size=25,
            legend_font_size=18,
            value_font_size=15)
        self.initAllGraphs()
    
    def initAllGraphs(self):
        self.generateMeanData()
        self.mean_chart = pygal.DateLine(x_label_rotation=25,style=self.custom_style)
        self.mean_chart.title = 'Mean site usage for ' + self.sitename
        self.mean_pngtitle = 'temp/' + (self.sitename).replace(' ','_') + 'mean.png'
        self.generateAsPNG(self.mean_chart,[["Mean",self.mean_data]],self.mean_pngtitle)

        plastic = []
        paper = []
        glass = []
        for entry in self.entries:
            plastic.append((entry[0],entry[2]))
            paper.append((entry[0],entry[3]))
            glass.append((entry[0],entry[4]))
        quicksort(plastic,0,len(plastic) - 1)
        quicksort(paper,0,len(paper) - 1)
        quicksort(glass,0,len(glass) - 1)

        self.usage_chart = pygal.DateLine(x_label_rotation=25,style=self.custom_style)
        self.usage_chart.title = 'Usage over time for ' + self.sitename
        self.usage_pngtitle = 'temp/' + (self.sitename).replace(' ','_') + '.png'
        self.generateAsPNG(self.usage_chart,[["Plastic",plastic],["Paper",paper],["Glass",glass]],self.usage_pngtitle)
    
    def graphConfigure(self,graphobj):
        graphobj.y_labels = self.y_values
        graphobj.x_labels = self.x_values
        graphobj.show_x_guides = True
        graphobj.show_y_guides = True
        graphobj.__init__

    def generateAsPNG(self,graphobj,data_arr,filename):
        self.graphConfigure(graphobj)
        for i in range(len(data_arr)):
            graphobj.add(data_arr[i][0],data_arr[i][1])
        graphobj.render_to_png(filename)

    def mean(self):
        n = len(self.entries)
        countplastic = 0
        countpaper = 0
        countglass = 0
        for i in range(len(self.entries)):
            countplastic += self.entries[i][2]
            countpaper += self.entries[i][3]
            countglass += self.entries[i][4]
        
        self.avr_plastic_usage = countplastic // n
        self.avr_paper_usage = countpaper // n
        self.avr_glass_usage = countglass // n

    def generateTotalMean(self):
        self.sum_each = [reduce((lambda x,y: x + y),[self.entries[i][2],self.entries[i][3],self.entries[i][4]]) for i in range(len(self.entries))]
        self.meanNums = list(map((lambda x: x // 3),self.sum_each))
        n = len(self.meanNums)
        sum_one = reduce((lambda x,y: x + y),self.meanNums)
        self.totalMean = sum_one // n

    def generateMeanData(self):
        self.generateTotalMean()
        self.mean_data = [[self.entries[i][0],self.meanNums[i]] for i in range(len(self.meanNums))]
        quicksort(self.mean_data,0,len(self.mean_data) - 1)
        self.mean()
    
    def getSiteProfile(self):
        sitevars = [self.totalMean,self.numPaper,self.numPlastic,self.numGlass,self.avr_paper_usage,self.avr_plastic_usage,self.avr_glass_usage]
        return [self.sitename,self.usage_pngtitle,self.mean_pngtitle,sitevars]

class weeklyAnalysis(Analysis):  # maybe add what percent it is at on the top of each bar chart
    def __init__(self, x_values, y_values, siteInfo, entries):
        self.graph_path = 'temp/' + (entries[0][1]).replace(' ','_') + '.png'
        super(weeklyAnalysis, self).__init__(x_values, y_values, siteInfo, entries)
        self.generateTotalMean()

    def normalDistributionOfWeeks(self):  # to get an avarage week i will use the normal distribution
        pass
        

    def initAllGraphs(self):
        self.x_values = [self.sitename]  # x value is different each time
        self.mean()
        if len(self.entries) > 1:
            self.entries = [[self.entries[0][0], self.entries[0][1], self.avr_plastic_usage, self.avr_paper_usage, self.avr_glass_usage]]
        
        self.main_chart = pygal.Bar()
        self.graphConfigure(self.main_chart)
        self.main_chart.add('Plastic', self.entries[0][2])
        self.main_chart.add('Paper', self.entries[0][3])
        self.main_chart.add('Glass', self.entries[0][4])
        self.main_chart.render_to_png(self.graph_path)
    
    #def initOtherValues(self):
        #self.generateTotalMean()

    def getSiteProfile(self):
        sitevars = [self.totalMean,self.numPaper,self.numPlastic,self.numGlass,self.avr_paper_usage,self.avr_plastic_usage,self.avr_glass_usage]
        return [self.sitename,self.graph_path,sitevars]

class monthlyAnalysis(Analysis):  # maybe not needed?? # work on as extra
    def __init__(self, title, x_values, y_values, siteInfo, entries):
        super(monthlyAnalysis, self).__init__(title, x_values, y_values, siteInfo, entries)

    def initAllGraphs(self):
        pass

    def getSiteProfile(self):
        pass

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
    
# maybe use a different method for the mean or just use the decimal?
# default to bar chart if there is only one value
# need to generate an 'avarage' week value

# from the other version before deleting:
#when using this on another computer, need to find the path of the current file name to save there
#callAnalysis(datetime.today().replace(day=1,month=1,hour=0, minute=0, second=0, microsecond=0),['Asda Ellis Way','Beeston Street','Pier','Boating lake'])
#callAnalysis(date(2020,11,1),['Asda Ellis Way','Beeston Street','Pier','Boating lake'])  # maybe i can make an advanced customisability at some point
# slightly problematically, pygal uses utc time by default -- might not cause any issues still

# have a 'this month feature', 'past 30 days feature'
# search the lists using re, regular expression
# sites to include must be alpha

#def generatereportpath(self,reporttype):    #  i think this would go into the report class
#today = (str((datetime.today()))[:-7]).replace(' ','_')
#filename = 'report' + '-' + date + '.pdf'
#path = '/home/livi/NEA/Past_Reports/' +

#need to sort the dates before appending so they are sorted in order

#this week vs the average week

#why does this run when i start it, do i need one of those if name = __main__
