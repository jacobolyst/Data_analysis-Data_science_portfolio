import requests
from bs4 import BeautifulSoup
import time

def main():
    '''Function for scraping links to the other words with getting the estimated time
    neede to end the process and number of links to scrap'''
    
    try:
        with open('nextWordListPage.txt', 'r') as f:
            wordsPageName = f.read()
    except:
        wordsPageName = 'https://pl.wiktionary.org/wiki/Kategoria:polski_(indeks)'
    linksFileName = 'wordsLinks.txt'
    links = []
    numberScrapped = 0
    timePassed = 0
    while wordsPageName is not None:
        try:
            newLinks = []
            
            t = time.time()
            response = requests.get(wordsPageName)
            soup = BeautifulSoup(response.content, 'html.parser')
            foundLinks = soup.find_all('a')

            wordsPageName = None

            opened = False
            for link in foundLinks:
                if link.text == 'następna strona':
                    if opened == False:
                        opened = True
                    else:
                        wordsPageName = 'https://pl.wiktionary.org'+link.get('href')
                        break
                elif link.text != 'poprzednia strona':
                    if opened == True:
                        newLinks.append(link.get('href'))        
            
            links.extend(newLinks)
            timePassedThisLoop = time.time()-t
            timePassed += timePassedThisLoop
            numberScrapped += 1
            if numberScrapped % 10 == 0:
                print(f"\n Scrapped {numberScrapped} pages, in average {timePassed/numberScrapped:.2f} seconds for each. \n Total time passed {timePassed:.2f}.\n")
        except:
            print(f"Error during scrapping of {wordsPageName}")
            break
    with open(linksFileName, 'a+') as file:
        for link in links:
            file.write('\n'+link)
    with open('nextWordListPage.txt', 'w') as file:
        if wordsPageName is not None:
            file.write(wordsPageName)
                
if __name__ == '__main__':
    main()