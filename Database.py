import psycopg2


def fetchLocations(port):  # for windows test inputting the port as host 
    con = psycopg2.connect(database="livi", user="livi", password="Pass1234",host=port)
    print("Database opened successfully")
    cur = con.cursor()
    cur.execute('''SELECT * FROM vw_locations;''')
    rows = cur.fetchall()
    con.close()
    #locations = list(rows[i][1] for i in range(len(rows)))
    #return locations
    return rows


def fetchSitedata(port):  # still need windows option
    con = psycopg2.connect(database="livi", user="livi", password="Pass1234",host=port)
    print("Database opened successfully")
    cur = con.cursor()
    cur.execute('''SELECT entryid,date,name,avrglass,avrpaper,avrplastic FROM sitedata
    INNER JOIN locations
    ON locationid = siteid
    ORDER BY name ASC;''')
    rows = cur.fetchall()
    con.close()
    return rows


def editExisting(port, inputdate, locationid, avrglass, avrpaper, avrplastic, entryID):
    con = psycopg2.connect(database="livi", user="livi", password="Pass1234",host=port)
    print("Database opened successfully")
    cur = con.cursor()
    print(inputdate)
    parameters = '''
    UPDATE sitedata 
    SET date = %s, locationid = %s, avrglass = %s, avrpaper = %s, avrplastic = %s
    WHERE entryid = %s;'''
    data = (str(inputdate), locationid, avrglass, avrpaper, avrplastic, entryID)
    cur.execute(parameters, data)
    con.commit()
    con.close()
