from flask import Flask,render_template,request

import bs4, requests, google


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
    app.debug = True
    app.run()
