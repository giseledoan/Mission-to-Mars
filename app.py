# use Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for

#use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo

#use the scraping code created to scrape the URL, image and table, saved in Mission-to-Mars folder
import scraping

#set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#tells Python that our app will connect to Mongo using a URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" # This URI is saying that the app can reach Mongo thru our localhost server, using port 27017, database named "mars_app".
mongo = PyMongo(app)

# define the route for the HTML page
# tells Flask what to display when we're looking at the home page, index.htm
@app.route("/")
def index():
    # find the "mars" collection in our database
    mars = mongo.db.mars.find_one()
    
    # tells Flask to return an HTML template using an index.html file
    return render_template("index.html", mars=mars) #mars=mars: tells Python to use the "mars" collection in MongoDB

# set up our scraping route. This route will be the "button" of the web application
# defines the route that Flask will be using. “/scrape”, will run the function created just beneath it.
@app.route("/scrape")
def scrape():
   # assign a new variable that points to our Mongo database
    mars = mongo.db.mars
    
    # reference the scrape_all function in the scraping.py file exported from Jupyter Notebook
    mars_data = scraping.scrape_all()
    
    # {}  empty JSON object to insert data from mars_data, upsert=True: create a new doc if one doesn't already exist
    mars.update({}, mars_data, upsert=True)
    
    # add a redirect after successfully scraping the data, navigate our page back to / where we can see the updated content
    return redirect('/', code=302)

#tell Flask to run
if __name__ == "__main__":
   app.run()
