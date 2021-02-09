
def extractSummaryBoxes(wanted):  # get tips on how to improve this
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
        return

extractSummaryBoxes(intsect)
