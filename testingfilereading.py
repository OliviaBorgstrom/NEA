import re
def extractSummaryBoxes(wanted):  # get tips on how to improve this
    arr_summary_box = []
    htmlfiles = []
    comparison_name = '2020-11-01_to_2021-02-01'.replace('_',' ')
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
                    htmldir = ('temp/' + site + '.html').replace(' ','_')
                    htmlfiles.append(htmldir)
                    for line in fh:
                        if line.strip() == '<div class=\"summary_box\" style=\"width:450px\">': 
                            break
                    f = open(htmldir,'w')
                    f.write('<b><u>Comparison report summary (' + comparison_name + ') </u><br></b>\n')
                    for line in fh:
                        if line.strip() == '</div>':
                            break
                        if not line.strip() == '<b>Number of bins:</b>' and not (line.strip())[:13] == '<!--IGNORE-->':
                            f.write(line)
                        arr_summary_box[i].append(line.strip())
                    f.close()
                    i += 1
    return arr_summary_box

def extractNumbers(string):
    print(string)
    return [int(s) for s in re.findall(r'\b\d+\b', string)]
    # using regular expressions to extract the numbers

sitesincluded = ['Boating Lake','Beeston Street','Asda Ellis Way']
with open('Past_html/2020-11-01_to_2021-02-01.html') as fh:
    first_line = fh.readline()
    sitesInComparison = ((first_line[5:-5]).replace(', ',',')).replace('\'','')
    sitesInComparison = sitesInComparison.split(',')
            
    l = set(sitesincluded)  # using sets to find the intersection and see if empty
    f = set(sitesInComparison)
    intsect = l.intersection(f)
    
    if not intsect:  # an empty set is intepreted as false
        # set comparing now false
        print('none in common')
    
    summary_boxes = extractSummaryBoxes(intsect)

    numbers= []
    for i in range(len(summary_boxes)):
        for j in range(len(summary_boxes[i])):
            found = extractNumbers(summary_boxes[i][j])
            if not len(found) == 0:
                numbers.append(extractNumbers(summary_boxes[i][j]))
    print(numbers)


