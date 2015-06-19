import MySQLdb, urllib, json, time

def connect_database(host, user, password, databasename):
    db = MySQLdb.connect(host = host,
                         user = user,
                         passwd = password,
                         db = databasename)
    
    return db


def parseCars(url):
    roster = urllib.urlopen(url)    #fetch from url
    roster = json.load(roster)      #parse into JSON
    
    roster = [i for i in roster if i["class_id"] == 3] #only want challengers

    return roster

def edit_db(value, column):
    cur.execute('''
    UPDATE wp_postmeta
    SET meta_value = %s
    WHERE meta_key = %s
    ''', (value, column))    


def create_markers(roster):
    string = """a:%s:{""" % \
        (str(len(roster)))
    
    
    for i in range(len(roster)):
        team_string = """i:%s;a:8:%s""" % \
            (str(i),
             create_team(roster[i]))
                
        string += team_string
    
    string += '}'
    return string


def create_team(data):
    string = """{s:5:"title";s:%s:"%s";s:11:"description";s:%s:"%s";s:9:"reference";s:0:"";s:12:"hide_details";b:0;s:3:"lat";s:%s:"%s";s:3:"lng";s:%s:"%s";s:6:"marker";s:0:"";s:5:"label";s:0:"";}""" % \
        (str(len(data['name'])), 
         data['name'], 
         
         str(len(str(data['dist_adelaide']))),
         str(data['dist_adelaide']),
         
         str(len(str(data['lat']))), 
         str(data['lat']), 
         
         str(len(str(data['lng']))), 
         str(data['lng']))
    
    return string
    

def generate_description(data):
    return



if __name__ == "__main__":
    
    db = connect_database('localhost', 'root', '', 'wordpress2')
   
   
    roster = parseCars('http://www.worldsolarchallenge.org/api/positions')

    markers = create_markers(roster)

    
    cur = db.cursor()
    
    edit_db(markers, 'gmb_markers_group')
    

 
   
    
    
    db.commit()
    
    cur.close()
    
       