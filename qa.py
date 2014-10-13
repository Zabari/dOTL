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

def findNames():
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
    s=f.read()
    f.close()
    #p=re.compile("(([A-Z][a-z]*)\s([A-Z][a-z]*))")
    #p=re.compile("([A-Z][a-z]*\s*){2,}")
    p=re.compile("([A-Z][a-z]*)\s([A-Z][a-z]*)")
    pre= p.findall(s)  
    r=re.compile('((?<![\.\!\?\"])(?<![\.\!\?\"\:\;]\s)(?<![\.\!\?\"\;\:]\s\s)[A-Z][a-z]+)')
    l=r.findall(s)
    for f in pre:
        for se in f:
            l.append(se)
    d={name: s.count(name) for name in l}
    #for name in r.findall(s):
    #    print name+":" +str(s.count(name))
    return d

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
    text=displayText(printLinks("who is Spiderman?",3))
    #print text
    f.write(str(text))
    f.close()
    print "done"
    print 
    print nameFind("out.txt")
    app.debug = True

    app.run()
