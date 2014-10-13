from flask import Flask,render_template,request

import google, requests, urllib2, re
from bs4 import BeautifulSoup


def printLinks(searchQuery, linksPerPage):
    s=google.search(searchQuery,tld='com',lang='en',num=10,start=0,stop=10,pause=2.0)
    count = 0;
    links = []
    for url in s:
        if count<linksPerPage:
            count=count+1
            #linkstring="\'"+url+"\'"
            links.append(url)
    return links

#not exactly sure how to open the url correctly
def displayText(links):
    linktext = ""
    for url in links:
        #urltext = urllib2.urlopen(url)
        r=requests.get(url)
        soup = BeautifulSoup(r.content)
        text=soup.prettify()
        #urltext.close()
        linktext += text.encode('utf-8')
    return linktext



def findNames(links):
    namelist = []
    for url in links:
        urltext = urllib2.urlopen(url)
        text = BeautifulSoup(urltext.read())
        urltext.close()
        templist = findnames(text.getText())
        for x in templist:
            if x not in namelist:
                namelist.append(x)
    return namelist

#using Terrance's code for now    

def findnames(d):
    data = d
    capital=re.findall('[A-Z]\w+',data)
    fullnames=re.findall('[A-Z]\w+ [A-Z]\w+', data)
    titles=re.findall("(?:Dr|Mr|Mrs|Ms|Prof)\.[A-Z]\w+",data)
    suffixes=re.findall("[A-Z]\w+ (?:Sr|Jr|PhD|MD)\.?",data)
    begofsent=re.findall("(?:\.|\?|\!)\s([A-Z]\w+)",data)
    f.close()
    names=[]
    appendnorep(fullnames,names)
    appendnorep(titles,names)
    appendnorep(suffixes,names)
    unsure=appeared(capital,names)
    for x in capital:
        if not appearwithin(x,names) and x not in begofsent:
            names.append(x)
            if x in unsure:
                unsure.remove(x)
    return names #+unsure

def appeared(unconf,conf):
    repeat=[]
    uns=[]
    for x in unconf:
        if appearwithin(x,conf):
            repeat.append(x)
    for x in unconf:
        if x not in repeat and x not in uns:
            uns.append(x)
    return uns

def appearwithin(x,group):
    for a in group:
        if x in a:
            return True
    return False

def appendnorep(list1,list2):
    for x in list1:
        if x not in list2:
            list2.append(x)
#end of Terrance's code
app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
@app.route("/home",methods=['GET','POST'])
def home():
    if request.method=="POST":
        searchQ = request.form["searchq"]
        n = int(request.form["nresults"])
        return render_template("results.html",n=n,s=searchQ,links=printLinks(searchQ,n))
    else:
        return render_template("home.html")

if __name__ == "__main__":
    f=open("out.txt","w")
    text=displayText(printLinks("hey",3))
    #print text
    f.write(str(text))
    f.close()
    print "done"
    app.debug = True

    app.run()