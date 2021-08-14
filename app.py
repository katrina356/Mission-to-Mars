# Line one use flask to render a template, redirect to a url and create a url
# line two use pymongo to interact with mongo database
# line three references our scraping file we created in jupyter and exported to py
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection. mars_app is the db we created in mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for the HTML page. line 1 tells Flask what to display when we'r looking at the home page
# def index uses PyMongo to find the "mars" collection in our db, assign path to Mars
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# this sets up the scraping route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

# this tells Flask to tell it to run
if __name__ == "__main__":
   app.run()