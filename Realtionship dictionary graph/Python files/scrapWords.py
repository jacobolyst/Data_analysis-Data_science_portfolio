import requests
from bs4 import BeautifulSoup
import time
import sys
import json
import pysondb
import pprint

def parseWordToDictionary(wordlink):
    '''Function which sends request to the Wiktionary site and downloads
    the headwords, cleans them with using Beautiful Soup and uncovers 
    definitions and type of the headword'''
    
    # Request to the server
    response = requests.get('https://pl.wiktionary.org' + wordlink)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Creating empty dictionary for the headwords
    definition = {}
    definition['definitions'] = {}
    definition['name'] = soup.span.text
    
    show = False
    # Inout definition of the headword
    definitionType = 'None'
    
    for i, tag in enumerate(soup.find_all(['dt', 'dd', 'p'])):
        # 'Znaczenia' in Polish means 'meanings'
        # Looking for the specific tags
        if tag.text == 'znaczenia:' and tag.name == 'dt':
            show = True
        
        elif tag.name == 'dt' and show:
            break
        
        else:
            if show == True:
                if tag.name == 'p':
                    # Cleaning from ',' and '\n' signs
                    definitionType = tag.text.split(',')[0].rstrip('\n')   
                
                else:
                    # Looking for the all definitions
                    tagChildrens = list(tag.children)
                    if tagChildrens:
                        definition['definitions'][tagChildrens[0]] = {}
                        definition['definitions'][tagChildrens[0]]['type'] = definitionType
                        definition['definitions'][tagChildrens[0]]['def.'] = []
                        
                        for children in tagChildrens[1:]:
                            if children != ' ' and children.name != 'link':
                                if children.name == 'span' or children.name == 'i':
                                    definition['definitions'][tagChildrens[0]]['def.'].append(children.text)
                                elif children.name != 'sup':
                                    definition['definitions'][tagChildrens[0]]['def.'].append(str(children))
    
    return definition


def scrapListOfWords(listOfLinksFileName, maxWords = None, dbName = None):
    '''Scarping the words from Wiktionary using above functions with
    getting the time of the whoe process and write after each 10 headwords
    the number of words to scrap and estimated time to finish '''
    
    with open(listOfLinksFileName, 'r') as file:
        listOfWords = file.readlines()
    if maxWords is not None:
        totalPages = maxWords
    else:
        totalPages = len(listOfWords)
    if dbName is not None:
        db = pysondb.db.getDb(dbName)
    #try:
    #    with open(databaseName, 'r') as db:
    #        database = json.loads(db.read())
    #except:
    #    database = {}
    try:
        timeElapsedParsing = 0
        timeElapsedFile = 0
        timeElapsedDB = 0
        for i, word in enumerate(listOfWords[:maxWords]):
            if i + 1 > totalPages:
                break
            t = time.time()
            definition = parseWordToDictionary(word.rstrip('\n'))
            #listOfWords.pop(word)
            timeElapsedParsing += time.time() - t
            
            t = time.time()
            if dbName is not None:
                definition['link'] = word.rstrip('\n')
                db.add(definition)
            timeElapsedDB += time.time() - t
            #else:
            t = time.time() 
            try:
                with open(word.rstrip('\n')[1:]+'.json', 'w') as f:
                    f.write(json.dumps(definition))
            except:
                try:
                    with open('notCompatibleLinkWordsDefinitions.json', 'r') as f:
                        content = f.read()
                    if content != '':
                        notCompDefs = json.loads(content)
                    else:
                        notCompDefs = {}
                except:
                    notCompDefs = {}
                definition['link'] = word.rstrip('\n')
                notCompDefs[word.rstrip('\n')] = definition
                #pprint.pprint(notCompDefs)
                with open('notCompatibleLinkWordsDefinitions.json', 'w') as f:
                    f.write(json.dumps(notCompDefs))
                with open("notCompatibleLinkWords.txt", "a+") as f:
                    f.write("\n"+word.rstrip('\n'))
            timeElapsedFile += time.time() - t
                    
            if (i + 1) % 10 == 0:
                print(f"Scrapped {i+1} pages, avg. {(timeElapsedParsing+timeElapsedDB+timeElapsedFile)/(i+1):.2f} seconds for each. ({timeElapsedParsing/(i+1):.2f} parsing, {timeElapsedFile/(i+1):.2f} file, {timeElapsedDB/(i+1):.2f} DB). \n Left {totalPages - i - 1} pages. Finish in {(totalPages - i - 1)*(timeElapsedParsing+timeElapsedDB+timeElapsedFile)/(i+1)/60/60:.2f} hours ({(totalPages - i - 1)*(timeElapsedParsing)/(i+1)/60/60:.2f} parsing, {(totalPages - i - 1)*(timeElapsedFile)/(i+1)/60/60:.2f} filee, {(totalPages - i - 1)*(timeElapsedDB)/(i+1)/60/60:.2f} DB).")

        with open(listOfLinksFileName, 'w') as file:
            file.writelines(listOfWords[i+1:])
    except:
        print(f"Encountered error in {word}.")
        with open(listOfLinksFileName, 'w') as file:
            file.writelines(listOfWords[i:])
        raise

        
def main():
    maxWords = None
    listOfLinksFileName = 'wordsLinksToScrap.txt'
    databaseName =  None#'wordsDB.json'
    try:
        maxWords = int(sys.argv[1])
    except:
        maxWords = None
    try:
        listOfLinksFileName = sys.argv[2]
    except:
        listOfLinksFileName = 'wordsLinksToScrap.txt'     
    #try:
    #    databaseName = sys.argv[3]
    #except:
    #    databaseName = "words.json"
    scrapListOfWords(listOfLinksFileName, maxWords = maxWords, dbName = databaseName)
    
if __name__ == '__main__':
    main()
    