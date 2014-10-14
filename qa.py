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
    f=open("out.txt","w")
    text=displayText(links)
    f.write(str(text))
    f.close()
    d= nameFind("out.txt")
    top1 = 0;
    top2 = 0;
    top3 = 0;
    topnames=["fill","fill","fill"]
    for x in d:
        if (d[x]>top1):
            top3 = top2
            top2 = top1
            top1 = d[x]
            topnames=[x,topnames[0],topnames[1]]
        elif (d[x]>top2):
            top3 = top2
            top2 = d[x]
            topnames=[topnames[0],x,topnames[1]]
        elif (d[x]>top3):
            top3 = d[x]
            topnames=[topnames[0],topnames[1],x]
    return topnames

#using Daniel's code
def nameFind(fil):
    f=open(fil,'r')
    data=f.read()
    f.close()
    capital=re.findall('[A-Z][a-z]+',data)
    fullnames=re.findall('[A-Z][a-z]+ [A-Z][a-z]+', data)
    titles=re.findall("(?:Dr|Mr|Mrs|Ms|Prof)\.[A-Z]\w+",data)
    suffixes=re.findall("[A-Z]\w+ (?:Sr|Jr|PhD|MD)\.?",data)
    begofsent=re.findall("(?:\.|\?|\!)\s([A-Z]\w+)",data)
    names=[]
    L=help()
    for x in capital:
        if x in L:
            names.append(x)
    d={name: data.count(name) for name in names}  
    s='''
    appendnorep(fullnames,names)
    appendnorep(titles,names)
    appendnorep(suffixes,names)
    unsure=appeared(capital,names)
    L=help()
    for x in capital:
        if not appearwithin(x,names) and x not in begofsent:
            names.append(x)
            if x in unsure:
                unsure.remove(x)
    d={name: data.count(name) for name in names}
    #for name in r.findall(s):
    #    print name+":" +str(s.count(name))
    '''
    
    return d

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

def help():
    f=open('names.txt','r')
    L=f.readlines()
    f.close()
    for i in range(len(L)):
        L[i]=L[i].title()[:-2]
    return L

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
@app.route("/home",methods=['GET','POST'])
def home():
    if request.method=="POST":
        searchQ = request.form["searchq"]
        n = int(request.form["nresults"])
        urllinks = printLinks(searchQ,n)
        return render_template("results.html",n=n,s=searchQ,results=findNames(urllinks),links=urllinks, namelist=nameFind("out.txt"))
    else:
        return render_template("home.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
