import psycopg2
from datetime import datetime

def fetchLocations(port):  # for windows test inputting the port as host
    con = psycopg2.connect(database="livi", user="livi", password="Pass1234",host=port)
    #print("Database opened successfully")

    cur = con.cursor()
    cur.execute('''SELECT * FROM locations;''')  # might want to add - order by name ASC (not sure if would break)
    rows = cur.fetchall()
    con.close()
    #locations = list(rows[i][1] for i in range(len(rows)))
    #return locations
    return rows

def fetchspecificLocations(port,sitelist):  # for windows test inputting the port as host
    con = psycopg2.connect(database="livi", user="livi", password="Pass1234",host=port)
    cur = con.cursor()
    parameters = '''SELECT * FROM locations
    WHERE name IN %s
    ORDER BY name ASC;'''
    cur.execute(parameters,(sitelist,))
    rows = cur.fetchall()
    con.close()
    return rows

def fetchbetweendates(port,datefrom,sitelist):
    con = psycopg2.connect(database="livi", user="livi", password="Pass1234",host=port)
    cur = con.cursor()
    
    parameters = '''SELECT date,name,avrpaper,avrplastic,avrglass FROM sitedata
    INNER JOIN locations
    ON locationid = siteid
    WHERE date BETWEEN %s AND %s
    AND name IN %s
    ORDER BY name ASC;'''
    cur.execute(parameters,(datefrom,datetime.today(),sitelist))
    rows = cur.fetchall()
    con.close()
    return rows

def fetchSitedata(port):  # still need windows option
    con = psycopg2.connect(database="livi", user="livi", password="Pass1234",host=port)
    #print("Database opened successfully")
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
    #print("Database opened successfully")
    cur = con.cursor()
    parameters = '''
    UPDATE sitedata
    SET date = %s, locationid = %s, avrglass = %s, avrpaper = %s, avrplastic = %s
    WHERE entryid = %s;'''
    data = (str(inputdate), locationid, avrglass, avrpaper, avrplastic, entryID)
    cur.execute(parameters, data)
    con.commit()
    con.close()

def addTo(port,inputdate, locationid, avrglass, avrpaper, avrplastic):
    con = psycopg2.connect(database="livi", user="livi", password="Pass1234",host=port)
    #print("Database opened successfully")
    cur = con.cursor()
    parameters = '''
    INSERT INTO sitedata(date,locationid,avrglass,avrpaper,avrplastic)
    VALUES(%s,%s,%s,%s,%s);'''
    data = (str(inputdate), locationid, avrglass, avrpaper, avrplastic)
    cur.execute(parameters, data)
    con.commit()
    con.close()

#i think it would break if the database was empty for sitedata
