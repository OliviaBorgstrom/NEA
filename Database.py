import psycopg2
from datetime import datetime

def deleteEntry(user,password,host,entryID):
    con = psycopg2.connect(database="livi", user=user, password=password,host=host)
    #print("Database opened successfully")
    cur = con.cursor()
    parameters = '''
    DELETE FROM sitedata
    WHERE entryid = %s;'''
    cur.execute(parameters, [entryID])
    con.commit()
    con.close()

def fetchLocations(user,password,host):  # for windows test inputting the port as host
    con = psycopg2.connect(database="livi", user=user, password=password,host=host)
    #print("Database opened successfully")

    cur = con.cursor()
    cur.execute('''SELECT * FROM locations
    ORDER BY name ASC;''')  # might want to add - order by name ASC (not sure if would break)
    rows = cur.fetchall()
    con.close()
    #locations = list(rows[i][1] for i in range(len(rows)))
    #return locations
    return rows

def fetchspecificLocations(user,password,host,sitelist):  # for windows test inputting the port as host
    con = psycopg2.connect(database="livi", user=user, password=password,host=host)
    cur = con.cursor()
    parameters = '''SELECT * FROM locations
    WHERE name IN %s
    ORDER BY name ASC;'''
    cur.execute(parameters,(sitelist,))
    rows = cur.fetchall()
    con.close()
    return rows

def fetchbetweendates(user,password,host,datefrom,sitelist):
    con = psycopg2.connect(database="livi", user=user, password=password,host=host)
    cur = con.cursor()
    print('Database opened')
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

def fetchSitedata(user,password,host):  # still need windows option
    con = psycopg2.connect(database="livi", user=user, password=password,host=host)
    #print("Database opened successfully")
    cur = con.cursor()
    cur.execute('''SELECT entryid,date,name,avrglass,avrpaper,avrplastic FROM sitedata
    INNER JOIN locations
    ON locationid = siteid
    ORDER BY name ASC;''')
    rows = cur.fetchall()
    con.close()
    return rows

def editExisting(user,password,host, inputdate, locationid, avrglass, avrpaper, avrplastic, entryID):
    con = psycopg2.connect(database="livi", user=user, password=password,host=host)
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

def addTo(user,password,host,inputdate, locationid, avrglass, avrpaper, avrplastic):
    con = psycopg2.connect(database="livi", user=user, password=password,host=host)
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
