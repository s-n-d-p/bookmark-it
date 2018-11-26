import os

import requests
from flask import Flask, render_template, request, redirect, url_for

from connection import session
from database_setup import Shortener

app = Flask(__name__)

def checkURI(uri, timeout=5):
	try:
		r = requests.get(uri,timeout=timeout)
		return r.status_code == 200
	except:
		return False

@app.route("/",methods=['GET','POST'])
def homepage():
	if request.method == 'GET':
		pass 
	elif request.method == 'POST':
		long_link = request.form['long_link'].encode('ascii','ignore')
		short_link = request.form['short_link'].encode('ascii','ignore')
		if session.query(Shortener).filter_by(short_link=short_link).scalar() is None:
			if checkURI(long_link):
				session.add(Shortener(short_link = short_link, long_link = long_link)) 	
				session.commit()
			else:
				return "Check the link again" 	
		else:
    		# It already exists in the database
			return "The short name already exists, try something else"
	else:
		pass 
	try:
		saved_urls = session.query(Shortener).all()
		return render_template("homepage.html",saved_urls=saved_urls)
	except:
		return render_template("homepage.html",saved_urls='')

@app.route("/<short_link>")
def redirectToURL(short_link):
	short_link = short_link.encode('ascii','ignore')
	if session.query(Shortener).filter_by(short_link = short_link).scalar() is not None:
		link = session.query(Shortener).filter_by(short_link = short_link).first().long_link.encode('ascii')
		return redirect(link)
	else:
		return 'Invalid short name'

def main():
	port = int(os.environ.get("PORT",8000))
	# app.debug = True
	app.run(host = "0.0.0.0", port = port)

if __name__ == "__main__":
	main()