import json
import pysondb

with open('wordsLinks.txt', 'r') as file:
   listOfWords = file.readlines()
   
#db = pysondb.db.getDb('wordsDB.json')

# Getting missing words

absentWords = []
for i, word in enumerate(listOfWords):
    try:
        with open(word.rstrip('\n')[1:]+'.json', 'r') as f:
            content = f.read()
        if content == "":
            absentWords.append(word)
    except:
        absentWords.append(word)
    if i % 1000 == 0:
        print(i)
        
with open('absentWords.txt.', 'w') as f:
    for word in absentWords:
        f.write(word)

print('Done')
# bilirubina