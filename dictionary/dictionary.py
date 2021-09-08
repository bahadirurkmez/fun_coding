import pandas as pd
import os
import json
import re
import difflib

## FIND SPLIT LOCATIONS
def findsplitlocs(content, pattern):
    p = re.compile(pattern) 
    result =[]
    for m in p.finditer(content):
        result.append(m.start())
    return result

## SPLIT TEXT and RETURN A LIST OF DESC
def splittext(text, splitlocs):

    returnlist = []
    if isinstance(splitlocs, list):
        for idx, element in enumerate(splitlocs):
            startloc = splitlocs[idx]
            endloc = splitlocs[(idx +1) % len(splitlocs)]
            returnlist.append(text[startloc:endloc -1])
    else:
        print ('splitlocs should be a list object')
        return None
    return returnlist

# SEARCH DICTIONARY
def getexplanation(searchText):
    if searchText.lower() in data:
        return data[searchText.lower()]
    else:
        # Check if user means a closer word or mistyped and get close matches
        return closematches(searchText.lower())


def closematches(strtomatch):
    matches = difflib.get_close_matches(strtomatch, data.keys(),n=5,cutoff=0.7)
    return (matches)

def printresult(result, desc):
    resulttext = result
    x = findsplitlocs(desc, '(\d+\.\s)+')
    if len(x) == 0:
        print(resulttext, ':')
        print(desc)
    else:
        y = splittext(desc, x)
        print(resulttext, ':')
        for item in y:
            print(item,'\n')
    
if os.path.exists('dict.json'):
    with open('dict.json') as f:
        data = json.load(f)

while True:
    search_word = input('Enter. an English word to learn its meaning:')

    description = getexplanation(search_word)

    if isinstance(description,list):
        if len(description) > 0:
            userconf =input('Word doesn\'t exist. Did you mean one of these %s instead? Y or N: ' % str(description))
            if userconf.lower() == 'y':
                userpref = int(input('Please enter the index of item starting from 1: '))
                if userpref < 1:
                    userpref = input('Please enter the index of item starting from 1. Index should be larger than 1: ')
                elif userpref + 1 > len(description):
                    userpref = input('Choice cannot be larger than %s' % len(description))
                else:
                    printresult(description[userpref-1],data[description[userpref-1]])
            elif userconf.lower() == 'n':
                print('To Quit press cntl + C\n')  
            else:
                print ('Word doesn\'t exist')
        else:
            print ('Word doesn\'t exist')
    else:          
        printresult(search_word,description)
   
    print('To Quit press cntl + C\n')    
        
