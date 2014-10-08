from flask import Flask,render_template,request
#import bs4, requests, google

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

#@app.route("/form",methods=['GET','POST'])

if __name__ == "__main__":
    app.debug = True
    app.run()
