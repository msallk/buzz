import cgi
import webapp2
import urllib
import json as simplejson
import time
import sys

from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Location(db.Model):
	location = db.StringProperty(required = True)
	time = db.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
    	locations = db.GqlQuery('SELECT * FROM Location ORDER BY time DESC')
    	values = {'locations': locations}
        self.response.out.write(template.render('main.html',values))
    def post(self):
    	location = Location(location = self.request.get('location'))
    	location.put()
        time.sleep(6)
        self.getXY(address = self.request.get('location'))
    	self.redirect('/');
        
    def getXY(self, address):
        coordinate = urllib.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address="+address+"&sensor=true")
        dict = simplejson.loads(coordinate.read())
        for result in dict["results"]: # result is a list of dictionaries 
            print("*",result["geometry"]["location"]["lat"],"\n")
            print("*",result["geometry"]["location"]["lng"],"\n")
            x=result["geometry"]["location"]["lat"]
            y=result["geometry"]["location"]["lng"]
            break
        return (x,y);


class Guestbook(webapp2.RequestHandler):
    def post(self):
        self.response.out.write('<html><body>You wrote:<pre>')
        self.response.out.write(cgi.escape(self.request.get('content')))
        self.response.out.write('</pre></body></html>')

app = webapp2.WSGIApplication([('/', MainPage),
                              ('/sign', Guestbook)],
                              debug=True)
