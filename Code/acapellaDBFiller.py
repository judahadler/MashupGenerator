# import required module
import os
from os import listdir
from os.path import isfile, join
import mariadb
import sys

##start Connect to MariaDB Platform ##
try:
    conn = mariadb.connect(
        user="elliottadler",
        password="",
        host="localhost",
        port=3306,
        database="test",
        autocommit=True

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

##End connection##


#test connection info
  #cur.execute("Show columns in instrumentals;")
# Print Result-set
    #for col in cur:
    #print(col)

# assign directory
dir_name = '/Users/elliottadler/Desktop/MUSIC/Music making/Mashup making/Mashup Material/Acapellas/'
# iterate over files in
# that directory

list_of_files = sorted( filter( lambda x: os.path.isfile(os.path.join(dir_name, x)),
                        os.listdir(dir_name) ) )

for filename in list_of_files:
    f = os.path.join(dir_name, filename)
    
    # checking if it is a file
    if os.path.isfile(f):

        #Skip over file Path (may need to do this smarter in case filepath isnt always 58 chars)
        f = f[len(dir_name)::]
        #print(f)

        #skip .dsstore file
        if f.startswith("."):
            continue

        # Get Tempo
        tempoList = f.split(" BPM")
        tempo = tempoList[0]
        

        #Get Key
        key = f[f.find('(')+1:f.find(')')]
        
        #Get artist
        artist = f.split('-')[1]
        artist = artist[:-1]
        artist = artist[1:]
        artist = artist.replace("_", " ")
        

        #Get Title
        title = f.split('-')[2]
        title = title[:-4]
        title = title[1:]

        #Clean up song title
        title = title.replace("_", " ")
        title = title.replace("Acapella", "")
        title = title.replace("acapella", "")
        title = title.replace("ACAPELLA", "")
        title = title.replace("Studio", "")
        title = title.replace("studio", "")
        title = title.replace("Official", "")
        title = title.replace("OFFICIAL", "")
        title = title.replace("official", "")
        title = title.replace("quality", "")
        title = title.replace("Quality", "")
        title = title.replace("audio", "")
        title = title.replace("Audio", "")
        title = title.replace("AUDIO", "")
        title = title.replace("(", "")
        title = title.replace(")", "")
        title = title.replace("[", "")
        title = title.replace("]", "")
        title = title.replace("getmp3.pro", "")
        title = title.replace("HQ", "")
        title = title.replace("Only", "")
        title = title.replace("only", "")
        title = title.replace("vocals", "")
        title = title.replace("Vocals", "")
        title = title.strip()

        #get release year (should use spotify api here)
        year = -1
        
        #get camelot  (should use spotify api here)
        cam = -1

        #assign type
        songType = "acapella"

        
        cur.execute("INSERT INTO instrumentals (bpm,artist,scale,title,release_year,camelot,type, downloaded) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (tempo, artist, key, title, year, cam, songType, True))


        

    

