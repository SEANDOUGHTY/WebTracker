import MySQLdb, urllib, json, time

def connect_database(host, user, password, databasename):
    db = MySQLdb.connect(host = host,
                         user = user,
                         passwd = password,
                         db = databasename)
    
    return db


def set_table(database, table):
    cur = database.cursor()
    cur.execute("SELECT * FROM " + table)   
    return cur


def parseCars(url):
    roster = urllib.urlopen(url)    #fetch from url
    roster = json.load(roster)      #parse into JSON
    
    roster = [i for i in roster if i["class_id"] == 3] #only want challengers

    return roster




if __name__ == "__main__":
    
    db = connect_database('localhost', 'root', '', 'wordpress2')
    
    #cur = set_table(db, 'wp_postmeta')
    
    roster = parseCars('http://www.worldsolarchallenge.org/api/positions')
    
    cur = db.cursor()
    
    cur.execute('''
    UPDATE wp_postmeta
    SET meta_value = 2
    WHERE meta_key = 'gmb_markers_group'
    ''')
    
    db.commit()
    
    cur.close()
    
       