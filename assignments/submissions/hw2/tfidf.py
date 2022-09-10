import re
from collections import Counter
import math
docs = []
preprocessed_docs = []

def initialize_docs():
    for line in (open('tfidf_docs.txt', 'r')):
        line = line.strip()
        docs.append(line)


def preprocessing():
    
    swFile = open('stopwords.txt', 'r')
    sws = swFile.readlines()
    stopwords = []
    for line in sws:
        stopwords.append(line.strip())
    swFile.close()
    #print(stopwords)
    
    for doc in docs:
        rowList = []
        file = open(doc, 'r')
        lines = file.readlines()
        for line in lines:
            #line = re.sub('^http[s]?://\S*','', line)
            line = re.sub(r'\b(http|https)://\S*','', line)
            line = re.sub('[^A-Za-z0-9_\s]','', line)
            line = re.sub('\s\s+',' ', line)
            line = line.lower().strip()
            words = line.split(' ')
            #print(words)
            words_new = [x for x in words if x not in stopwords]
            #print(words_new)
            line = ' '.join(words_new)
            line = re.sub(r'ing\b','',line)
            line = re.sub(r'ly\b','',line)
            line = re.sub(r'ment\b','',line)
            rowList.append(line)
        
        file.close()
        newfile = 'preproc_' + doc
        preprocessed_docs.append(newfile)
        file_out = open(newfile, 'w')
        #for line in rowList:
         #   file_out.write(line + ' ')
            
        for i in range(len(rowList)):
            if i != (len(rowList) - 1 ):
                file_out.write(rowList[i] + ' ')
            else:
                file_out.write(rowList[i])
            
        file_out.close()
     
def computing():
    
    list_of_wfreq = []
    list_of_tfreq = []
    list_of_idf = []
    list_of_tfidf = []
    
    
    for doc in preprocessed_docs:
        file = open(doc, 'r')
        lines = file.readlines()
        words = []
        for line in lines:
            wordsInLine = line.split(' ')
            words.extend(wordsInLine)
        
        wfreq = Counter(words)
        list_of_wfreq.append(wfreq)
        
    #print(list_of_wfreq)
    
    for d in list_of_wfreq:
        total = 0.0
        tfreq = {}
        for value in d.values():
            total+=value
        
        for key, value in d.items():
            tfreq[key] = value/total
            
        list_of_tfreq.append(tfreq)
        
    print('Term Frequencies')
    print(list_of_tfreq)
    print('\n\n\n')
    #IDF[t] = (Total number of documents)/(Number of documents the word is found in)
    
    total_doc_num = len(preprocessed_docs)
    

    for d in list_of_wfreq:
        #a particular document
        
        #key: dictinct word, value: # of documents it occurs in
        num_docs_word = {}
        for key in d.keys():
            #calculate the number of documents word occurs in
            num = 0
            for i_d in list_of_wfreq:
                if key in i_d.keys():
                    num += 1
            
            num_docs_word[key] = num
            
        idf = {}
        for key in d.keys():
            if num_docs_word[key] != 0:
                idf[key] = math.log(total_doc_num/num_docs_word[key])+1
            else:
                idf[key] = 1
                
        list_of_idf.append(idf)
    
    print('IDFS')
    print(list_of_idf)
    print('\n\n\n')
    
    for i in range(len(list_of_wfreq)):
        #one particular document
        d = list_of_wfreq[i]
       
        tfidf = {}
        for key in d.keys():
            #each distinct word
            tfidf[key] = round((list_of_tfreq[i][key] * list_of_idf[i][key]), 2)
        
        list_of_tfidf.append(tfidf)
    
    print('TFIDFS')
    print(list_of_tfidf)
    print('\n\n\n')
        
    for d in list_of_tfidf:
        d_sorted = sorted(d.items(), key=lambda item: (-item[1], item[0]))  
        print(d_sorted)
        i = list_of_tfidf.index(d)
        n = 5
        if len(d_sorted) < 5:
            n = len(d_sorted)
        d_sorted = d_sorted[:n]  
        
        newfile = 'tfidf_' + docs[i]
        file_out = open(newfile, 'w')
        #file_out.write('[' + ','.join(d_sorted) +']')
        file_out.write(str(d_sorted))
        file_out.close()
        
    
    
        
#testing
initialize_docs()
print(docs)
preprocessing()
computing()

        
