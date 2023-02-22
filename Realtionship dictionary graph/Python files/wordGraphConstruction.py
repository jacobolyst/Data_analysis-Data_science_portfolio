import networkx as nx
from getEdges import convertEdgesFileToList
import time

def constructWordGraph():
    '''Construct the Directed Graph with all words based on 
    edges created from the list with words from .txt file'''
    
    edges = convertEdgesFileToList()
    with open('wordsLinks.txt', 'r') as file:
        listOfWords = file.readlines()
    wordGraph = nx.DiGraph()
    
    for edge in edges:
        wordGraph.add_edge(edge[0], edge[1])
    
    for word in listOfWords:
        if not word.rstrip('\n') in wordGraph:
            wordGraph.add_node(word.rstrip('\n'))
    
    return wordGraph
    
    
def loadWordGraph():
    return nx.read_edgelist('wordGraph.txt')
    
    
def main():
    wordGraph = constructWordGraph()
    nx.write_edgelist(wordGraph, 'wordGraph.txt')
    
    
def compareSpeed():
    MC = 5
    loadTime = time.time()
    for i in range(MC):
        print(i)
        loadWordGraph()
    loadTime = (time.time() - loadTime)/MC
    
    constructTime = time.time()
    for i in range(MC):
        print(i)
        constructWordGraph()
    constructTime = (time.time() - constructTime)/MC
    
    # loading 6.30 sec., constructing 8.79
    print(f'Loading time: {loadTime:.2f}. Constructing time: {constructTime:.2f}')

    
if __name__ == '__main__':
    main()