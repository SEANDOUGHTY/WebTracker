import MySQLdb, urllib, json, time

'''
These global variables are need to configure your current environment to run
the WebTracker
'''

'''
host = '127.0.0.1'
user = 'wordpressuser739'
password = 't2[%Ch8lFw5T'
databasename = 'wordpress739'
map_id = 1797
post_title = 'Test'
'''

#Sean's Computer
host = 'localhost'
user = 'root'
password = ''
databasename = 'wordpress4'
map_id = 6
image_root = 'http://localhost/wordpressblue2/wp-content/uploads/2015/10/'
post_title = 'Test'


#nick's Computer
"""
host = '127.0.0.1'
user = 'root'
password = ''
databasename = 'wordpress'
map_id = 4
url = 'http://www.worldsolarchallenge.org/api/positions'
name = 'Blue Sky Solar Racing'
post_title = 'Track Our Progress'
"""

control_stop = [{'name': 'testing', 'description': 'test', 'lat': -34.922809, 'lng': 138.601913}]

url = 'http://www.worldsolarchallenge.org/api/positions'
name = 'Blue Sky Solar Racing'

def connect_database(host, user, password, databasename):
    '''
    Takes database info and connects to the MySQL database
    '''
    
    db = MySQLdb.connect(host = host,
                         user = user,
                         passwd = password,
                         db = databasename)
    
    return db


def parseCars(url):
    '''
    Takes url and parses the cars using .json
    '''
    
    roster = urllib.urlopen(url)    #fetch from url
    roster = json.load(roster)      #parse into JSON
    
    roster = [i for i in roster if i["class_id"] == 5] #only want challengers
    
    return roster

def blue_last(roster):
    '''
    Modifies roster and returns it with blue sky solar at the end
    '''
    
    for i in range(len(roster)):
        if roster[i]['name'] == name:
            roster[-1], roster[i] = roster[i], roster[-1]
    
    return roster    

def find_blue_remaining(roster):
    for i in range(len(roster)):
        if roster[i]['name'] == name:
            return roster[i]['dist_adelaide']
    

def edit_map(value, column):
    '''
    Function that will change a 'column' of wp_postmeta to 'value'
    '''
    
    cur.execute('''
    UPDATE wp_postmeta
    SET meta_value = %s
    WHERE meta_key = %s
    ''', (value, column))    

def edit_scrollbar(value, column):
    cur.execute('''
    UPDATE wp_posts
    SET post_content = %s
    WHERE post_title = %s
    ''', (value, column))    

def create_scrollbar(roster, map_id):
    string = '''
    <div id="map">
    [google_maps id="%s"] 
    </div>

    <div id="scrollbar">''' % (map_id)
    
    flagDict = {
        'ca':('Canada','canadian-flag.jpg'),
    	'us':('United States of America','american-flag.jpg'),
    	'ph':('Phillipines','filipino-flag.jpg'),
    	'nl':('Netherlands','dutch-flag.jpg'),
    	'cn':('China','chinese-flag.jpg'),
    	'jp':('Japan','japanese-flag.jpg'),
    	'hk':('Hong Kong','chinese-flag.jpg'),
    	'de':('Germany','german-flag.jpg'),
    	'nz':('New Zealand','new-zealander-flag.jpg'),
    	'sg':('Singapore','singaporean-flag.jpg'),
    	'au':('Australia','australian-flag.jpg'),
    	'id':('Indonesia','indonesian-flag.jpg'),
    	'tr':('Turkey','turkish-flag.jpg'),
    	'my':('Malaysia','malaysian-flag.jpg'),
    	'it':('Italy','italian-flag.jpg'),
    	'be':('Belgium','belgian-flag.jpg'),
    	'co':('Colombia','colombian-flag.jpg'),
    	'tw':('Taiwan','taiwan-flag.jpg'),
    	'se':('Sweden','swedish-flag.jpg'),
        'ch':('Switzerland','swiss-flag.jpg'),
        'cl':('Chile','chilean-flag.jpg'),
        'kr':('South Korea','south-korean-flag.jpg'),
        'gb':('Great Britain','great-britan-flag.jpg')
    }
    
    for i in range(len(roster)):
        curCar = roster[i]
        curCarCountry = roster[i]['country']
        if curCarCountry in flagDict:
            string += create_team_scrollbar(curCar, i, find_blue_remaining(roster), flagDict[curCarCountry][0], (image_root + flagDict[curCarCountry][1]))
        else:
            string += create_team_scrollbar(curCar, i, find_blue_remaining(roster), 'not found', 'not found')
            
    string += '</div>'
    
    return string


def create_markers(roster, blue_remaining):
    '''
    Creates all the markers that will show on the map usign syntax that the
    GMB plugin understands
    '''
    
    
    string = """a:%s:{""" % \
        (str(len(roster)+len(control_stop)))
    
    for i in range(len(roster) - 1):            #for loop to add all teams
        team_string = """i:%s;a:8:%s""" % \
            (str(i),
             create_team(roster[i], blue_remaining))
                
        string += team_string
        print(i)
        
    string += """i:%s;a:8:""" % \
        (str(len(roster)-1)) + \
        create_blue(roster[-1]) #special function to add BSS
    
    for i in range(len(control_stop)):
        control_string = """i:%s;a:8:%s""" % \
            ((len(roster) + i),
             create_control(control_stop[i]))
        
        string += control_string
    
    string += '}'
    return string

def create_blue(data):
    '''
    Function to create the BSS marker
    '''
    
    description = generate_description(data, 0, True)
    
    string = """{s:5:"title";s:%s:"%s";s:11:"description";s:%s:"%s";s:9:"reference";s:0:"";s:12:"hide_details";b:0;s:3:"lat";s:%s:"%s";s:3:"lng";s:%s:"%s";s:6:"marker";s:108:"{ path : MAP_PIN, fillColor : "#428BCA", fillOpacity : 1, strokeColor : "", strokeWeight: 0, scale : 1 / 3 }";s:5:"label";s:0:"";}""" % \
            (str(len(data['name'])), 
             data['name'], 
             
             len(description),
             description,
             
             str(len(str(data['lat']))), 
             str(data['lat']), 
             
             str(len(str(data['lng']))), 
             str(data['lng']))
        
    return string    

def create_team(data, blue_remaining):
    '''
    Function to create a generaic team
    '''
    
    description = generate_description(data, blue_remaining, False)

    string = """{s:5:"title";s:%s:"%s";s:11:"description";s:%s:"%s";s:9:"reference";s:0:"";s:12:"hide_details";b:0;s:3:"lat";s:%s:"%s";s:3:"lng";s:%s:"%s";s:6:"marker";s:0:"";s:5:"label";s:0:"";}""" % \
        (str(len(data['name'])), 
         data['name'], 
         
         len(description),
         description,
         
         str(len(str(data['lat']))), 
         str(data['lat']), 
         
         str(len(str(data['lng']))), 
         str(data['lng']))
    
    return string

def create_control(data):
    '''
    Function to create a generaic control stop
    '''

    string = """{s:5:"title";s:%s:"%s";s:11:"description";s:%s:"%s";s:9:"reference";s:0:"";s:12:"hide_details";b:0;s:3:"lat";s:%s:"%s";s:3:"lng";s:%s:"%s";s:6:"marker";s:0:"";s:5:"label";s:0:"";}""" % \
        (str(len(data['name'])), 
         data['name'], 
         
         str(len(str(data['description']))), 
         str(data['description']),
         
         str(len(str(data['lat']))), 
         str(data['lat']), 
         
         str(len(str(data['lng']))), 
         str(data['lng']))
    
    return string


def create_team_scrollbar(data, place, blue_remaining, carCountryFull, carCountryImg):
    if carCountryFull != 'not found':
        string = '''
         <div class="leaderboard">
        <p>%s - %s</p>
        <p>To Adelaide: %skm</p>
        <p>From Blue Sky %skm</p>
        <p>Country: %s</p>
        <center><img src="%s" alt="%s"></center>
         </div> ''' % \
                    (place_string(place),
                     data['name'],
                     distance_shorten(data['dist_adelaide']),
                     distance_shorten(data['dist_adelaide'] - blue_remaining),
                     carCountryFull,
                     carCountryImg,
                     carCountryFull)
        
    else:
        string = '''
         <div class="leaderboard">
        <p>%s - %s</p>
        <p>To Adelaide: %skm</p>
        <p>From Blue Sky %skm</p>
        
         </div> ''' % \
                    (place_string(place),
                     data['name'],
                     distance_shorten(data['dist_adelaide']),
                     distance_shorten(data['dist_adelaide'] - blue_remaining)
                     )
    
    return string
                    
                    
def place_string(number):
    number = str(number + 1)
    
    if number[-1] == 1:
        return number + 'st'
    if number[-1] == 2:
        return number + 'nd'
    if number[-1] == 3:
        return number + 'rd'
    return number + 'th'
    
def distance_shorten(distance):
    distance = str(distance)
    distance = distance[:distance.find('.')]
    return distance

def generate_description(data, blue_remaining, blue):
    '''
    Function to generate box description for each team
    '''
    
    if not blue:
        desc = '''Distance from Darwin: %skm</br>Distance to Adelaide: %skm</br>Distance from Blue Sky Solar Racing: %skm''' % \
            (data['dist_darwin'],
             data['dist_adelaide'],
             data['dist_adelaide'] - blue_remaining)
        return desc
    
    desc = '''Distance from Darwin: %skm</br>Distance to Adelaide: %skm''' % \
               (data['dist_darwin'],
                data['dist_adelaide'])    
    return desc


def set_center(data):
    '''
    Function to set the pan to where BSS is
    '''
    
    string = '''a:2:{s:8:"latitude";s:%s:"%s";s:9:"longitude";s:%s:"%s";}''' % \
        (str(len(str(data['lat']))),
         str(data['lat']),
         
         str(len(str(data['lng']))),
         str(data['lng']))
    
    edit_map(string, 'gmb_lat_lng')





if __name__ == "__main__":
    
    db = connect_database(host, user, password, databasename)
    cur = db.cursor()
   
   # roster = parseCars(url)
   #bypass mode
    roster = open("positions.txt", "r")    #fetch from url
    roster = json.load(roster)      #parse into JSON
   
    roster = [i for i in roster if i["class_id"] == 5] #only want challengers


    
    scrollbar = create_scrollbar(roster, map_id)
    edit_scrollbar(scrollbar, post_title)




    roster = blue_last(roster)

    set_center(roster[-1])


    markers = create_markers(roster, roster[-1]['dist_adelaide'])

    
       
    edit_map(markers, 'gmb_markers_group')
    

 
   
    
    
    db.commit()
    
    cur.close()
    
       
