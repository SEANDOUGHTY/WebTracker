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

host = '127.0.0.1'
user = 'root'
password = ''
databasename = 'wordpress'
map_id = 4
url = 'http://www.worldsolarchallenge.org/api/positions'
name = 'Blue Sky Solar Racing'
post_title = 'i fkin love darwin'


control_stop = [{'name': 'Control Stop 1', 'description': 'Katherine', 'lat': -14.4666667, 'lng': 132.2666667},
                {'name': 'Control Stop 2', 'description': 'Dunmarra', 'lat': -16.67983333, 'lng': 133.41188889},
                {'name': 'Control Stop 3', 'description': 'Tennant Creek', 'lat': -19.65775, 'lng': 134.1885},
                {'name': 'Control Stop 4', 'description': 'Barow Creek', 'lat': -21.5319444, 'lng': 133.8888889},
                {'name': 'Control Stop 5', 'description': 'Alice Springs', 'lat': -23.70861111, 'lng': 133.87555556},
                {'name': 'Control Stop 6', 'description': 'Kulgera', 'lat': -25.83911111, 'lng': 133.31572222},
                {'name': 'Control Stop 7', 'description': 'Coober Pedy', 'lat': -29.01105556, 'lng': 134.75466667},
                {'name': 'Control Stop 8', 'description': 'Glendambo', 'lat': -30.96986111, 'lng': 135.749},
                {'name': 'Control Stop 9', 'description': 'Port Augusta', 'lat': -32.50919444, 'lng': 137.79672222}
                ]


start_end = [{'name': 'Start: Darwin', 'description': 'State Square, Darwin', 'lat': -12.46305556, 'lng': 130.83780556},
             {'name': 'Finish: Adelaide', 'description': 'Victoria Square, Adelaide ', 'lat': -34.9306000, 'lng':  138.6042000}
             ]

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

    string += '''
              <p>Track the progress of Horizon as we race 3000km across the Australian outback!
              Make sure to keep up with our social media pages, which can be found at the bottom of this webpage.</p>
              '''
    
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


def getFinishedTeamsRoster(roster):
    '''
    looks to see if any teams are finished and adds them to the beginning of the roster
    '''

    finishedFile = open('finishedTeams.txt','w+') #load the file that shows the teams that finished the race
    finishedTeams = json.load(finishedFile)       #..and parse them into an array of dictionaries
    
    for j in range(len(roster)):                 #look through each item in the roster and determine if they are finished
        #if the team is finished but not on the finishedList, add and remove from roster
        if not any (finishedTeams['name'] == roster[i]['name']) && roster[i]['dist_adelaide'] < 1.0:                 
               finishedTeams.append(roster[i])
               del roster[i]
        else if any(finishedTeams['name'] == roster[i]['name']):    #else, remove from roster
               del roster[i]

    roster = finishedTeams + roster              #then append all the finished teams to the beginning of the roster, we should have the correct order now
    finishedFile.write(str(finishedTeams))       #you do not need to truncate the file before re writing the list of dictionaries because opening in w+ mode does so.
    
    finishedFile.close()
    
    return roster

if __name__ == "__main__":
    
    db = connect_database(host, user, password, databasename)
    cur = db.cursor()
   
   # roster = parseCars(url)
   #bypass mode
    roster = open("positions.txt", "r")    #fetch from url
    roster = json.load(roster)      #parse into JSON
   
    roster = [i for i in roster if i["class_id"] == 5] #only want challengers

    
    roster = getFinishedTeamsRoster(roster)
    scrollbar = create_scrollbar(roster, map_id)

    
    edit_scrollbar(scrollbar, post_title)

    roster = blue_last(roster)

    set_center(roster[-1])

    markers = create_markers(roster, roster[-1]['dist_adelaide'])

    
       
    edit_map(markers, 'gmb_markers_group')
    

 
   
    
    
    db.commit()
    
    cur.close()
    
       
