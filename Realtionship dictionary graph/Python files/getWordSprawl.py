import networkx as nx
from wordGraphConstruction import constructWordGraph
import time
import multiprocessing as mp
import sys
'''
def getWordSprawl(word, aggregate, wordGraph, visited):
    if (word in aggregate.keys()) == False:
        aggregate[word] = []
        definedWords = wordGraph.predecessors(word)
        for definedWord in definedWords:
            print(definedWord)
            aggregate[word].append(definedWords)
            if (definedWord in visited) == False:
                visited.append(definedWord)
                aggregate[word].extend(getWordSprawl(definedWord, aggregate, wordGraph, visited))
        aggregate[word] = list(set(aggregate[word]))      
    return aggregate[word]
'''

def getWordSprawl(word, wordGraph):
    '''Counting the return path to the word (self-loop definitions)'''
    
    count = 0
    to_itself = False
    for node in list(wordGraph.nodes):
        if nx.has_path(wordGraph, node, word):
            count += 1  
    return count - 1
    
def getWordListSprawl(listOfLinksFileName, maxWords = None, savingFile = 'wordSprawl.txt'):
    '''Getting the self loop definitions - when we start to search other words
    describe the one word and looking for the connection and return to this one
    from other headwords'''
    
    with open(listOfLinksFileName, 'r') as file:
        listOfWords = file.readlines()  
    if maxWords is not None:
        totalPages = maxWords
    else:
        totalPages = len(listOfWords)
    try:
        wordGraph = constructWordGraph()
        t = time.time()
        for i, word in enumerate(listOfWords[:maxWords]):
            if i + 1 > totalPages:
                break
            sprawl = getWordSprawl(word.rstrip('\n'), wordGraph)
            
            with open(savingFile, 'a+') as f:
                f.write(str((word.rstrip('\n'), sprawl))+'\n')
                    
            if (i + 1) % 10 == 0:
                currentT = time.time()
                print(f"Calculated {i+1} pages, avg. {(currentT-t)/(i+1):.2f} seconds for each. \n Left {totalPages - i - 1} pages. Finish in {(totalPages - i - 1)*(currentT-t)/(i+1)/60/60:.2f} hours.")

        with open(listOfLinksFileName, 'w') as file:
            file.writelines(listOfWords[i+1:])
    except:
        print(f"Encountered error in {word}.")
        with open(listOfLinksFileName, 'w') as file:
            file.writelines(listOfWords[i:])
        raise
        

def tests():
    word = '/wiki/fragment'
    aggregate = {}
    wordGraph = constructWordGraph()
    visited = [word]
    #print('Going to calculate sprawl')
    #getWordSprawl(word, aggregate, wordGraph, visited)
    #print(aggregate)
    has_path = False
    path = None
    for neighbor in wordGraph.successors(word):
        has_path = nx.has_path(wordGraph, neighbor, word)
        if has_path: 
            path = nx.shortest_path(wordGraph, source=neighbor, target=word)
            break
    print(word,has_path)
    print(path)
    word = '/wiki/dobry'
    has_path = False
    path = None
    for neighbor in wordGraph.successors(word):
        has_path = nx.has_path(wordGraph, neighbor, word)
        if has_path: 
            path = nx.shortest_path(wordGraph, source=neighbor, target=word)
            break
    print(word,has_path)
    print(path)
    
    word = '/wiki/kupa'
    has_path = False
    path = None
    for neighbor in wordGraph.successors(word):
        has_path = nx.has_path(wordGraph, neighbor, word)
        if has_path: 
            path = nx.shortest_path(wordGraph, source=neighbor, target=word)
            break
    print(word,has_path)
    print(path)
    
    word = '/wiki/w'
    count = 0
    for node in list(wordGraph.nodes):
        if node == word:
            print(node)
        if nx.has_path(wordGraph, node, word):
            count += 1
    print(count)
    
def main():
    maxWords = None
    listOfLinksFileName = 'wordsLinksToSprawl.txt'
    databaseName =  None#'wordsDB.json'
    try:
        maxWords = int(sys.argv[1])
    except:
        maxWords = None
    try:
        listOfLinksFileName = sys.argv[2]
    except:
        listOfLinksFileName = 'wordsLinksToSprawlKuba.txt'     
    try:
        savingFile = sys.argv[3]
    except:
        savingFile = 'wordSprawlKuba.txt'   
    getWordListSprawl(listOfLinksFileName, maxWords = maxWords, savingFile = savingFile)

if __name__ == '__main__':
    main()
