import re
import math
import string
import textract
import os.path
from bs4 import BeautifulSoup

def readFile(filename):
    extension = os.path.splitext(filename)[1]
    if extension == ".html":
        f = open(filename)
        text = f.read()
        f.close()
        return text
    if extension in ['.pdf', '.docx', '.jpg', '.jpeg', '.png', '.gif']:
    text = textract.process(filename)
    return text

def extract_flight(filename):
    text = readFile(filename)
    #pnr
    print re.search(r'[A-Z0-9]{6}', text).group()
    #passenger name
    print re.search(r'MR\. (\w*) (\w*)', text).group()
    #flight number
    print re.search(r'[A-Z0-9][A-Z0-9] \d\d\d', text).group()
    #date
    print re.search(r'[A-Z][a-z]{2} [0-9]{2} [A-Z][a-z]{2}, 20[0-9]{2}',text).group()
    #arr, dep time
    time_tuples = re.findall(r'\d+:\d\d [AP]M', text)
    for row in time_tuples:
        ept_time = time_tuples[0]
        arr_time = time_tuples[1]
            print dept_time, '->', arr_time

def extract_train(filename):
    text = readFile(filename)
    #pnr
    print re.search(r'<span>([0-9]{10})</span>', text).group(1)
    #passenger name
    name_tuples = re.findall(r'<td(.*)>([A-Z]+ [A-Z]+)</td>', text)
    for row in name_tuples:
        (attb, name) = row
        print name #train number, name
        print re.search(r'<span>([0-9]{5} / [A-Z\s]+)</span>', text).group(1)
        #scheduled departure
        print re.search(r'[0-9]+-[A-Z][a-z]{2}-20[0-9]{2}', text).group(), ' ',
        re.search(r'[0-9]{2}:[0-9]{2}', text).group()

def idf(keyword):
    totalDocs = float(len(files))
    relDocsCount = 0.0
    for i in range(len(soup)):
        title = [word.strip(string.punctuation).lower()
        for word in soup[i].title.string.split()]
            heading = [word.strip(string.punctuation).lower()
            for word in soup[i].h2.string.split()]
                paragraph = [word.strip(string.punctuation).lower()
                for word in soup[i].p.string.split()]
                    for word in title:
                        if word == keyword:
                            relDocsCount+=1 break
                        else:
                            for word in heading:
                                if word == keyword: relDocsCount+=1
                                break
                            else:
                                for word in paragraph:
                                    if relDocsCount == 0:
                                        return 0
                                    if word == keyword: relDocsCount+=1
                                        break
                                    else:
                                        return math.log((totalDocs+1)/(relDocsCount))

def scorePage(hotSoup, keywords): #keywords: list of keywords
    title = [word.strip(string.punctuation).lower() for word in hotSoup.title.string.split()]
    heading = [word.strip(string.punctuation).lower() for word in hotSoup.h2.string.split()]
    paragraph = [word.strip(string.punctuation).lower() for word in hotSoup.p.string.split()]
    keywords = [word.strip(string.punctuation).lower() for word in keywords]
    tkt = 'n'
    if ('flight' in heading):
        tkt = 'fl'
    elif ('train' in heading):
        tkt = 'tr'
    score = 0.0
    relevance = 0.0
    length = len(title) + len(heading) + len(paragraph)
    for keyword in keywords:
        for word in title:
            if word == keyword:
            relevance+=1
            score+=2
        for word in heading:
            if word == keyword:
                relevance+=1
                score+=3
        for word in paragraph:
            if word == keyword:
                relevance+=1
        score+=1 #score*=(idf(keyword))
        score *= relevance/length return [score, tkt]   #return score and ticket status

def scoreDoc(text, keywords):
    paragraph = [word.strip(string.punctuation).lower() for word in text.split()] keywords]
    keywords = [word.strip(string.punctuation).lower() for word in  tkt = 'n' #no ticket
                if ('flight' in paragraph):
                    tkt = 'fl' #flight
                elif ('train' in paragraph):
                    tkt = 'tr'
                score = 0.0 relevance = 0.0
                length = len(paragraph)
                for keyword in keywords:
                    for word in paragraph:
                        if word == keyword:
                            relevance+=1
                            score+=1
                    score *= relevance/length return [score, tkt]
                #return score and ticket status
                
#main
#TODO: ADD INDIVIDUAL NAMES
files = ['doc0.docx', 'doc1.docx', 'doc2.docx', 'page0.html', 'page1.html', 'page2.html', 'doc3.docx', 'page3.html', 'page4.html', 'page5.html','page6.html', 'page7.html', 'page8.html', 'page9.html', 'try.pdf', 'picture.png', 'picture2.png', 'ppt1.pptx']
soup = []
#list of files`
#list of BeautifulSoup objects
#parse [files] and convert to BeautifulSoup objects
    for i in range(len(files)):
        soup.append(BeautifulSoup(open(files[i]), 'html.parser'))
        keywords = [word.strip(string.punctuation).lower() for word in raw_input('Search here: ').split()]
                #list of keywords
                #is user looking for trains or flights?
            wantFlight = False
            wantTrain = False
        if 'flights' in keywords or 'flight' in keywords or 'plane' in keywords:
            wantFlight = True
            if 'trains' in keywords or 'train' in keywords or 'irctc' in keywords:
                wantTrain = True
                if 'trips' in keywords:
                    wantFlight = True
                    wantTrain = True scores = {}
page
tickets = {}
l = []
#stores file name against score of
#stores file name against ticket status #stores result of scorePage function
#assign scores according to algorithm to each file
for i in range(len(files)):
                extension = os.path.splitext(files[i])[1]
                if extension == ".html":
                    hotSoup = BeautifulSoup(open(files[i]), 'html.parser') l = scorePage(hotSoup,keywords)
                    scores[files[i]] = l[0]
                    tickets[files[i]] = l[1]
                elif extension in ['.pdf', '.docx', '.jpg', '.jpeg', '.png', '.gif']:
                    l=scoreDoc(readFile(files[i]), keywords)
                    scores[files[i]] = l[0]
                    tickets[files[i]] = l[1]
#display files and scores, sorted by score
                
                
border = '********************'
for file in sorted(scores, key=scores.get, reverse=True):
    if wantFlight == True and tickets[file] == 'fl': print border + '\n', file extract_flight(file)
                print border
    elif wantTrain == True and tickets[file] == 'tr':
                print border + '\n', file extract_train(file)
                print border
    else:
                print file, scores[file]














