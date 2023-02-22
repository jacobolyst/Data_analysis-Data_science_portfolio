from bs4 import BeautifulSoup
import time
import sys
import json
    
def convertToEdgesOfWords(listOfLinksFileName, maxWords = None):
    '''Creting a list with headwords with one or more definition, scapping
    a sign (1.1 or 2.1 or 1.2) and type of the word and getting the direct
    link to it'''
    
    with open(listOfLinksFileName, 'r') as file:
        listOfWords = file.readlines()
    
    if maxWords is not None:
        totalPages = maxWords
    else:
        totalPages = len(listOfWords)
    
    try:
        timeElapsedParsing = 0
        timeElapsedFile = 0
        for i, word in enumerate(listOfWords[:maxWords]):
            if i + 1 > totalPages:
                break
            t = time.time()
            
            try:
                with open(word.rstrip('\n')[1:]+'.json', 'r') as f:
                    definition = json.loads(f.read())
            except:
                with open('notCompatibleLinkWordsDefinitions.json', 'r') as f:
                    definition = json.loads(f.read())
                definition = definition[word.rstrip('\n')]
            
            edges = []
            
            for definition_key in definition['definitions'].keys():
                definingWords = definition['definitions'][definition_key]['def.']
                #print(definingWords)
                for defWord in definingWords:
                    link = BeautifulSoup(defWord, 'html.parser')
                    link = link.find_all('a')
                    if link:    
                        try:
                            link = link[0].get('href')
                            if link[0:5] == '/wiki':
                                edges.append((word.rstrip('\n'), link, definition_key.rstrip(' '), definition['definitions'][definition_key]['type']))
                        except:
                            pass
                        
            timeElapsedParsing += time.time() - t
            t = time.time() 
            
            with open('edgesList.txt', 'a+', encoding="utf-8") as f:
                for edge in edges:
                    f.write('\n'+str(edge))
            timeElapsedFile += time.time() - t
                    
            if (i + 1) % 100 == 0:
                #, avg. {(timeElapsedParsing+timeElapsedFile)/(i+1):.4f} seconds for each. ({timeElapsedParsing/(i+1):.4f} parsing, {timeElapsedFile/(i+1):.4f} file)
                print(f"Converted {i+1} pages. \n Left {totalPages - i - 1} pages. Finish in {(totalPages - i - 1)*(timeElapsedParsing+timeElapsedFile)/(i+1)/60:.2f} minutes ({(totalPages - i - 1)*(timeElapsedParsing)/(i+1)/60:.2f} parsing, {(totalPages - i - 1)*(timeElapsedFile)/(i+1)/60:.2f} file).")

        with open(listOfLinksFileName, 'w') as file:
            file.writelines(listOfWords[i+1:])
    except:
        print(f"Encountered error in {word}.")
        with open(listOfLinksFileName, 'w') as file:
            file.writelines(listOfWords[i:])
        raise
        
        
def main():
    maxWords = None
    listOfLinksFileName = 'wordsLinksToEdges.txt'
    try:
        maxWords = int(sys.argv[1])
    except:
        maxWords = None
    try:
        listOfLinksFileName = sys.argv[2]
    except:
        listOfLinksFileName = 'wordsLinksToEdges.txt'   
    
    convertToEdgesOfWords(listOfLinksFileName, maxWords = maxWords)
    
def convertEdgesFileToList():
    with open('edgesList.txt', 'r', encoding="utf-8") as f:
        edges = f.readlines()
    listOfEdges = []
    listOfEdges.append(eval(edges[0].rstrip('\n')))
    for edge in edges[1:]:
        listOfEdges.append(eval(edge.rstrip('\n')))
    return listOfEdges
    
if __name__ == '__main__':
    main()
