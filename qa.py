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

@app.route("/")
@app.route("/home")
def home():
    searchQ="Who is Spiderman?"
    n = 10
    return render_template("home.html",n=n,s=searchQ,links=printLinks(searchQ,n))

#@app.route("/form",methods=['GET','POST'])

if __name__ == "__main__":
    app.debug = True
    app.run()
