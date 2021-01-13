# do some analysing!
# import numpy
# from Database import ... # will need to make some new functions for this?
import matplotlib

class graphobj(object):
    def __init__(self,data,title):
        self.data = data
        self.title = plt.title(title)

        x = [1,2,3]
        y = [2,4,1]
        self.xlabel = plt.xlabel('x - axis')
        self.ylabel = plt.ylabel('y - axis')

graph1 = graphobj('insert data','a test graph')
plt.show()
