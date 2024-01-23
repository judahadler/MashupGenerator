
import mariadb
import sys

#shifts = {'c': }

#Use these to calculate how much we need to pitch shift a song
note_values = {
    'C': 1,
    'C#': 2,
    'Db': 2,
    'D': 3,
    'D#': 4,
    'Eb': 4,
    'E': 5,
    'F': 6,
    'F#': 7,
    'Gb': 7,
    'G': 8,
    'G#': 9,
    'Ab': 9,
    'A': 10,
    'A#': 11,
    'Bb': 11,
    'B': 12
}

#Finds Relative major/minor for the provided scale
def getRelativeScale(scale):

    list = []

    # split the key into components of note + maj/min
    m = "m"
    scale = scale.lower()
    brokenDown = scale.split('m')
    
    letter = brokenDown[0]
    relative = m + brokenDown[1]

    #If we have a major scale, get its minor equivalent
    if relative == "maj":
        
        if letter == "c":
            list.append("amin")
        if letter == "db" or letter == "c#":
            list.append("bbmin")
            list.append("a#min")
        if letter == "d":
            list.append("bmin")
        if letter == "d#" or letter == "eb":
            list.append("cmin")
        if letter == "e":
            list.append("c#min")
            list.append("dbmin")
        if letter == "f":
            list.append("dmin")
        if letter == "f#" or letter == "gb":
            list.append("dmin")
        if letter == "g":
            list.append("emin")
        if letter == "g#" or letter == "ab":
            list.append("fmin")
        if letter == "a":
            list.append("f#min")
            list.append("gbmin")
        if letter == "a#" or letter == "bb":
            list.append("gmin")
        if letter == "b":
            list.append("g#min")
            list.append("abmin")

    # If we have a minor scale, get its major equivalent
    if relative == "min":
        if letter == "c":
            list.append("ebmaj")
            list.append("d#maj")
        if letter == "db" or letter == "c#":
            list.append("emaj")
        if letter == "d":
            list.append("fmaj")
        if letter == "d#" or letter == "eb":
            list.append("f#maj")
            list.append("gbmaj")
        if letter == "e":
            list.append("gmaj")
        if letter == "f":
            list.append("abmaj")
            list.append("g#maj")
        if letter == "f#" or letter == "gb":
            list.append("amaj")
        if letter == "g":
            list.append("bbmaj")
            list.append("a#maj")
        if letter == "g#" or letter == "ab":
            list.append("bmaj")
        if letter == "a":
            list.append("cmaj")
        if letter == "a#" or letter == "bb":
            list.append("dbmaj")
            list.append("c#maj")
        if letter == "b":
            list.append("dmaj")

    return list


#Get all adjacent keys up to 2 scales up or down
def findAdjacentKeys(scale):
    result = []
    m = "m"
    scale = scale.lower()
    brokenDown = scale.split('m')
    letter = brokenDown[0]
    relative = m + brokenDown[1]

    if relative == "maj":
        if letter == "c":
            result.append(("c#maj", 1))
            result.append(("bmaj", -1))
        if letter == "db" or letter == "c#":
            result.append(("cmaj", -1))
            result.append(("dmaj", 1))
        if letter == "d":
            result.append(("c#maj", -1))
            result.append(("d#maj", 1))
        if letter == "d#" or letter == "eb":
            result.append(("dmaj", -1))
            result.append(("emaj", 1))
        if letter == "e":
            result.append(("d#maj", -1))
            result.append(("fmaj", 1))
        if letter == "f":
            result.append(("emaj", -1))
            result.append(("f#maj", 1))
        if letter == "f#" or letter == "gb":
            result.append(("fmaj", -1))
            result.append(("gmaj", 1))
        if letter == "g":
            result.append(("f#maj", -1))
            result.append(("g#maj", 1))
        if letter == "g#" or letter == "ab":
            result.append(("amaj", 1))
            result.append(("gmaj", -1))
        if letter == "a":
            result.append(("g#maj", -1))
            result.append(("a#maj", 1))
        if letter == "a#" or letter == "bb":
            result.append(("amaj", -1))
            result.append(("bmaj", 1))
        if letter == "b":
            result.append(("a#maj", -1))
            result.append(("cmaj", 1))

    if relative == "min":
        if letter == "c":
            result.append(("c#min", 1))
            result.append(("bmin", -1))
        if letter == "db" or letter == "c#":
            result.append(("cmin", -1))
            result.append(("dmin", 1))
        if letter == "d":
            result.append(("c#min", -1))
            result.append(("d#min", 1))
        if letter == "d#" or letter == "eb":
            result.append(("dmin", -1))
            result.append(("emin", 1))
        if letter == "e":
            result.append(("d#min", -1))
            result.append(("fmin", 1))
        if letter == "f":
            result.append(("emin", -1))
            result.append(("f#min", 1))
        if letter == "f#" or letter == "gb":
            result.append(("fmin", -1))
            result.append(("gmin", 1))
        if letter == "g":
            result.append(("f#min", -1))
            result.append(("g#min", 1))
        if letter == "g#" or letter == "ab":
            result.append(("amin", 1))
            result.append(("gmin", -1))
        if letter == "a":
            result.append(("g#min", -1))
            result.append(("a#min", 1))
        if letter == "a#" or letter == "bb":
            result.append(("amin", -1))
            result.append(("bmin", 1))
        if letter == "b":
            result.append(("a#min", -1))
            result.append(("cmin", 1))

    print(result)
    return result

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

song = input("What Instrumental are you using?\n-")

cur.execute(
    "SELECT scale, bpm FROM Instrumentals WHERE title=?", 
    (song,))

allScales = []
tempScales = []
flattenedAllScales = []
scale = ""

# Print Result-set
for (row) in cur:
    print(row)
    scale = row[0]
    bpm = row[1]

moreKeys = input("Would you like to expand your search by more keys? (Y/N)\n-")

if moreKeys == 'Y' or moreKeys == 'y':

    newKeys = findAdjacentKeys(scale)
    print(f"scale = [{scale}]")
    newKeys.append((scale, 0))
    print(f"newKeys = [{newKeys}]")
    for key, shift in newKeys:
        tempScales.append((getRelativeScale(key), shift))

    print(f"tempScales = [{tempScales}]")
    for scaleList, shift in tempScales:
        if len(scaleList) == 1:
            allScales.append((scaleList[0], shift))
        else:
            allScales.append((scaleList[0], shift))
            allScales.append((scaleList[1], shift))

    print(f"AllScales1 = [{allScales}]")
    for tup in newKeys:
        allScales.append(tup)
    print(f"AllScales2 = [{allScales}]")

    for scale, shift in allScales:
        flattenedAllScales.append(scale)

    print(f"Looking for songs in {flattenedAllScales} - {song}'s tempo is {bpm} and scale is {scale}")
    print("_________________________________________________________")


    for scale, shift in allScales:
        scale.split('m')

        cur.execute(
            "SELECT title, artist, bpm FROM Instrumentals WHERE scale =? AND type=?",
            (scale, "acapella",))

        for (row) in cur:
            title = row[0]
            artist = row[1]
            tempo = row[2]

            if abs(int(tempo) - int(bpm)) <= 15:
                print(f"Title: [{title}], by: [{artist}], Tempo = [{tempo}], Shift it [{shift}] semitones")
            if abs(int(tempo * 2) - int(bpm)) <= 15:
                print(f"Title: [{title}], by: [{artist}], Tempo = [{tempo}], Shift it [{shift}] semitones")
            if abs(int(tempo) - int(bpm * 2)) <= 15:
                print(f"Title: [{title}], by: [{artist}], Tempo = [{tempo}], Shift it [{shift}] semitones")

else:
    relativeScale = getRelativeScale(scale)

    print(f"Looking for songs in [{scale}] or {relativeScale} - {song}'s tempo is {bpm}")
    print("_________________________________________________________")

    if len(relativeScale) > 1:
        cur.execute(
        "SELECT title, artist, bpm FROM Instrumentals WHERE (scale=? OR scale=? OR scale=?) AND type=?",
        (scale, relativeScale[0], relativeScale[1], "acapella",))
    else:
        cur.execute(
            "SELECT title, artist, bpm FROM Instrumentals WHERE type=? AND (scale=? OR scale=?)",
            ("acapella",scale, relativeScale[0],))

    for (row) in cur:
        title = row[0]
        artist = row[1]
        tempo = row[2]
        print(f"Title: [{title}], by: [{artist}], Tempo = [{tempo}]")
        if abs(int(tempo) - int(bpm)) <= 15:
            print("GREAT FIT!")
        if abs(int(tempo * 2) - int(bpm)) <= 15:
            print("GREAT FIT!")
        if abs(int(tempo) - int(bpm * 2)) <= 15:
            print("GREAT FIT!")




