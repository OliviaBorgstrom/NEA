from sorting_alg import quicksort
from Database import fetchspecificLocations, fetchbetweendates
from datetime import datetime, date, timedelta
import pygal
from collections import OrderedDict
import math
from functools import reduce
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pygal.style import Style,CleanStyle

class Report(object):
    def __init__(self,dateto,datefrom,filteredlocations,sitestoinclude,host):
        self.dataObjects = []
        self.templatepath = 'path'
        self.datefrom = datefrom
        self.dateto = dateto
        self.sitestoinclude = sitestoinclude
        self.filteredlocations = filteredlocations
        self.host = host

        self.title = 'An Analysis of Bring To Site Usage Between ' + str(datefrom) + ' and ' + str(dateto)
        self.template_vars = {}
        self.template_vars['title'] = self.title

        self.y_values = list(i for i in range(0, 110,10))
        self.num_months = (self.dateto.year - self.datefrom.year) * 12 + (self.dateto.month - self.datefrom.month)
        if self.num_months == 0:
            self.num_days = self.dateto.day - self.datefrom.day
            if self.num_days <= 7:
                self.generatex_values_weekly()
                self.initAnalysisObj(weeklyAnalysis)
            else:
                self.generatex_values_monthly()
                self.initAnalysisObj(monthlyAnalysis)
        else:
            self.generatex_values()
            self.initAnalysisObj(Analysis)
        
        self.generateOverallSummary()
        self.renderhtml('dummypath')

    def initAnalysisObj(self, AnalysisClass):  # can add a thing at the bottom saying -> no data found for ...
        self.sitestoinclude = tuple(self.sitestoinclude)
        sitedata = fetchbetweendates('desktop','password',self.host,self.datefrom,self.sitestoinclude)  # filtering out locations where no data is found
        available_sites = [site[1] for site in sitedata]  # site 1 is the name
        sitesincluded = list(OrderedDict.fromkeys(available_sites))  # dictionaries cant have any duplicates so useful here

        sitedata_split = self.sublists(sitesincluded,sitedata,available_sites) 

        for i in range(len(sitesincluded)):
            self.dataObjects.append(AnalysisClass('Analysis',self.x_values,self.y_values,self.filteredlocations[i],sitedata_split[i]))
        
        sitevars = [[each.totalMean,each.numPaper,each.numPlastic,each.numGlass,each.avr_paper_usage,each.avr_plastic_usage,each.avr_glass_usage] for each in self.dataObjects]
        sites = [[self.dataObjects[i].sitename,self.dataObjects[i].usage_pngtitle,self.dataObjects[i].mean_pngtitle,sitevars[i]] for i in range(len(self.dataObjects))]
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
        self.months = array_circ(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],(datetime.today().month - 1))
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
        line_chart.render_to_png('Overallbarchart.png')
        self.template_vars['barchart'] = 'Overallbarchart.png'
        
    def generatereportpath(self):
        pass
    
    def renderhtml(self,templatepath):
        env = Environment(loader=FileSystemLoader('.'))
        self.template = env.get_template("html_templates/mainReport.html")
        print(self.template_vars)
        html_out = self.template.render(self.template_vars)
        HTML(string=html_out,base_url=__file__).write_pdf("report.pdf",stylesheets=["html_templates/style.css"])

class Analysis(object):  # those which arent specifically monthly or weekly are just Analysis
    def __init__(self, title, x_values, y_values, siteInfo, entries):
        self.title = 'title'
        self.x_values = x_values
        self.y_values = y_values
        self.sitename = siteInfo[1]
        self.numPlastic = siteInfo[2] 
        self.numPaper = siteInfo[3] # number of bins of each type
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
        self.mean_pngtitle = (self.sitename).replace(' ','_') + 'mean.png'
        self.generateAsPNG(self.mean_chart,[["Mean",self.mean_data]],self.mean_pngtitle)

        plastic = []
        paper = []
        glass = []
        for entry in self.entries:
            plastic.append((entry[0],entry[2]))
            paper.append((entry[0],entry[3]))
            glass.append((entry[0],entry[4]))
        quicksort(plastic,0,len(plastic)-1)
        quicksort(paper,0,len(paper)-1)
        quicksort(glass,0,len(glass)-1)

        self.usage_chart = pygal.DateLine(x_label_rotation=25,style=self.custom_style)
        self.usage_chart.title = 'Usage over time for ' + self.sitename
        self.usage_pngtitle = (self.sitename).replace(' ','_') + '.png'
        self.generateAsPNG(self.usage_chart,[["Plastic",plastic],["Paper",paper],["Glass",glass]],self.usage_pngtitle)
    
    def generateAsPNG(self,graphobj,data_arr,filename):
        graphobj.y_labels = self.y_values
        graphobj.x_labels = self.x_values
        graphobj.show_x_guides = True
        graphobj.show_y_guides = True
        graphobj.__init__

        for i in range(len(data_arr)):
            graphobj.add(data_arr[i][0],data_arr[i][1])
        
        graphobj.render_to_png(filename)
    
    def generateMeanData(self):
        sum_each = [reduce((lambda x,y: x + y),[self.entries[i][2],self.entries[i][3],self.entries[i][4]]) for i in range(len(self.entries))]
        meanNums = list(map((lambda x: x // 3),sum_each))
        self.mean_data = [[self.entries[i][0],meanNums[i]] for i in range(len(meanNums))]
        quicksort(self.mean_data,0,len(self.mean_data)-1)

        n = len(meanNums)
        sum_one = reduce((lambda x,y: x + y),meanNums)
        self.totalMean = sum_one // n

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

class weeklyAnalysis(Analysis):
    def __init__(self, title, x_values, y_values, siteInfo, entries):
        super(weeklyAnalysis, self).__init__(title, x_values, y_values, siteInfo, entries)
    
    def initAllGraphs(self):
        pass

class monthlyAnalysis(Analysis):
    def __init__(self, title, x_values, y_values, siteInfo, entries):
        super(monthlyAnalysis, self).__init__(title, x_values, y_values, siteInfo, entries)
    
    def initAllGraphs(self):
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
    
