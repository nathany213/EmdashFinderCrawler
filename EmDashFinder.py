##########################  ##########################
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
########################## global vars ##########################
checkedLinks = set() #faster than list, but doesnt keep order of list
newLinks = []
finalInfo = []
prevLinkLength = 1
isFirstPrint = True
startTime = 0
########################## functions ##########################
def findStr(str, txt):
    count = 0
    instances = []
    for i in range(len(txt)):
        if txt[i] == str:
            count += 1
            #finds sentence that the str was in
            a = i
            while txt[a] != "." and a > i - 500 and a > -len(txt) + 1: #finds previous sentence end
                a -= 1
            preContext = txt[a:i]
            a = i
            while txt[a] != "." and a < i + 500 and a < len(txt) - 1: #finds next sentence start
                a += 1
            postContext = txt[i:a]
            context = preContext + postContext

            instances.append([i, count, context]) #character index, 1st to last em dash, sentence it was in
    if len(instances) > 0:
        return instances
    else:
        return

def cleanLink(link):
    link = urlparse(link)
    link = f"https://{link.netloc}{link.path}"
    link = link.rstrip("/")
    return link

def getPageInfo(pageLink, totalLinks):
    global prevLinkLength
    global isFirstPrint
    global startTime

    cleanedPageLink = cleanLink(pageLink)
    checkedLinks.add(cleanedPageLink) #replace into checkedlinks

    timeElapsed = time.time() - startTime 
    timeElapsed = round(timeElapsed)
    if timeElapsed < 60:
        formattedTimeElapsed = f"{timeElapsed} secs"
    elif timeElapsed < 3600:
        formattedTimeElapsed = f"{timeElapsed // 60} mins, {timeElapsed % 60} secs"
    else:
        formattedTimeElapsed = f"{timeElapsed // 3600} hours, {timeElapsed // 60} mins, {timeElapsed % 60} secs"
    if len(newLinks) == 0:
        if len(checkedLinks) <= 0:
            percentage = "0%" #just started the sequence
        else:
            percentage = "100%" #finished, since newlinks would be empty at the end
    else:
        percentage = f"{(len(checkedLinks)/(totalLinks)) * 100:.2f}%"


    statusMsg = f"crawled {len(checkedLinks)}/{totalLinks}, {percentage} | Time elapsed: {formattedTimeElapsed} | currently crawling: {cleanedPageLink}"
    
    if isFirstPrint: #if is first time printing, print normally
        print(statusMsg)
        isFirstPrint = False
    else: #otherwise, print should overwirte 
          #the previous line so that it looks better
        print(f"\033[A\r\033[K{statusMsg}")
    
    response = requests.get(cleanedPageLink)
    prevLinkLength = len(pageLink)
    parsedUrl = urlparse(response.url)
    baseUrl = f'https://{parsedUrl.netloc}/{parsedUrl.path}'
    ogHtml = response.text
    soup = BeautifulSoup(ogHtml, "html.parser")
    pageText = soup.get_text() #only text, no tags and stuff

    for link in soup.find_all("a", href=True):
        fullLink = urljoin(cleanedPageLink, link.get("href"))
        cleanedLink = cleanLink(fullLink)

        if baseUrl in cleanedLink: #check if the link is for this site
            if cleanedLink not in checkedLinks and cleanedLink not in newLinks:
                newLinks.append(cleanedLink) #add to newlinks only if not checked already
    results = findStr("—", pageText) 
    if results != None:
        finalInfo.append([cleanedPageLink, results])


def checkAllPages(firstPageLink):
    global startTime

    startTime = time.time()
    cleanedFirstPageLink = cleanLink(firstPageLink)
    newLinks.append(cleanedFirstPageLink)

    while len(newLinks) > 0:
        totalUniqueLinks = len(newLinks) + len(checkedLinks)
        currentLink = newLinks.pop(0) #.pop gets the value of a item and also deletes it
        getPageInfo(currentLink, totalUniqueLinks)

    totalEmDashes = 0
    for page in finalInfo:
        dashesOnPage = len(page[1])
        totalEmDashes += dashesOnPage
    print("")
    print("")
    print(f'{totalEmDashes} em dashes found across {len(checkedLinks)} pages')
    #print(finalInfo)
    for pageUrl, matches in finalInfo:
        print("")
        print(pageUrl)
        for i, count, context in matches:
            formattedContent = " ".join(context.split())
            print(f"em-dash number {count}")
            print(f"context:")
            print(formattedContent)
            print("")


########################## actual code ##########################

print("")
print("")
print("Em Dash Finder, made by me (Nathan/nathany100)")
selectedSite = input("input your starting page:")
checkAllPages(selectedSite)

#https://quotes.toscrape.com
#https://englishan.com/em-dash/