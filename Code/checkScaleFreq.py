import os
from os import listdir
from os.path import isfile, join
import sys


def getRelativeScale(letter):
    # If we have a minor scale, get its major equivalent
    if letter == "c":
        return "d#maj"
    if letter == "db" or letter == "c#":
        return "emaj"
    if letter == "d":
        return "fmaj"
    if letter == "d#" or letter == "eb":
        return "f#maj"
    if letter == "e":
        return "gmaj"
    if letter == "f":
        return "g#maj"
    if letter == "f#" or letter == "gb":
        return "amaj"
    if letter == "g":
        return "a#maj"
    if letter == "g#" or letter == "ab":
        return "bmaj"
    if letter == "a":
        return "cmaj"
    if letter == "a#" or letter == "bb":
        return "c#maj"
    if letter == "b":
        return "dmaj"

    return "BLAHHHH"

def convertToSharp(letter):
    convert = ""
    if letter == "bb":
        convert = "a#"
    if letter == "ab":
        convert = "g#"
    if letter == "gb":
        convert = "f#"
    if letter == "eb":
        convert = "d#"
    if letter == "db":
        convert = "c#"

    return convert

def checkScales(dir_name, scaleToCheck):

    # iterate over files in that directory
    list_of_files = sorted(filter(lambda x: os.path.isfile(os.path.join(dir_name, x)),
                                  os.listdir(dir_name)))

    keyList = {"cmaj" : 0,
               "c#maj" : 0,
               "dmaj" : 0,
               "d#maj" : 0,
               "emaj" : 0,
               "fmaj" : 0,
               "f#maj" : 0,
               "gmaj" : 0,
               "g#maj" : 0,
               "amaj" : 0,
               "a#maj" : 0,
               "bmaj" : 0,
               }
    songsByKey = {"cmaj" : [""],
               "c#maj" : [""],
               "dmaj" : [""],
               "d#maj" : [""],
               "emaj" : [""],
               "fmaj" : [""],
               "f#maj" : [""],
               "gmaj" : [""],
               "g#maj" : [""],
               "amaj" : [""],
               "a#maj" : [""],
               "bmaj" : [""]}

    for filename in list_of_files:
        f = os.path.join(dir_name, filename)

        # checking if it is a file
        if os.path.isfile(f):

            # Skip over file Path (may need to do this smarter in case filepath isnt always 58 chars)
            f = f[len(dir_name)::]
            #print(f)

            # skip .dsstore file
            if f.startswith("."):
                continue

            # Get Tempo
            tempoList = f.split(" BPM")
            tempo = tempoList[0]

            # Get Key
            key = f[f.find('(') + 1:f.find(')')]
            # split the key into components of note + maj/min
            m = "m"
            scale = key.lower()
            brokenDown = scale.split('m')

            if len(brokenDown) < 2:
                continue

            letter = brokenDown[0]
            relative = m + brokenDown[1]

            if relative == "min":
                #print("found min")
                scale = getRelativeScale(letter)

            newBrokenDown = scale.split('m')
            newLetter = newBrokenDown[0]

            if len(newLetter) > 1:
                if newLetter[1] == 'b':
                    #print("found flat")
                    #print(scale)
                    newestLetter = convertToSharp(newLetter)
                    scale = newestLetter + "maj"

            #print(scale)

            keyList.update({scale: keyList.get(scale) + 1})
            #print(songsByKey.get(scale))
            songsByKey[scale] += [f]

    print(keyList)
    #print(songsByKey)
    #print(sum(keyList.values()))
    #print(*songsByKey["g#maj"], sep='\n')
    return songsByKey[scaleToCheck]

#d#maj': 4, 'emaj': 4, 'fmaj': 3, 'g#maj': 9


# assign directory
inst_dir = '/Users/elliottadler/Desktop/MUSIC/Music making/Mashup making/Mashup Material/Instrumentals/'
aca_dir = '/Users/elliottadler/Desktop/MUSIC/Music making/Mashup making/Mashup Material/Hebrew Acapella/'
aca1_dir = '/Users/elliottadler/Desktop/MUSIC/Music making/Mashup making/Mashup Material/Hebrew Acapella/Vol 1/'
acaNoah_dir = '/Users/elliottadler/Desktop/Noah/'
print(*checkScales(acaNoah_dir,"d#maj"), sep='\n')