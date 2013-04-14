import cgi
import webapp2
import urllib
import json
import time
import sys

from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Tweet(db.Model):
    location = db.StringProperty(required = True)
    category = db.StringProperty(required = True)
    content = db.StringProperty(required = False, multiline = True)
    image = db.StringProperty(required = False)
    username = db.StringProperty(required = False)
    time = db.DateTimeProperty(auto_now_add = True)



class MainPage(webapp2.RequestHandler):
    def get(self):
    	res = db.GqlQuery('SELECT * FROM Tweet')
        result = []
        for r in res:
            result.append((r.content, r.image, r.username))
    	results = {'tweets': result}
        self.response.out.write(template.render('main.html', results))
    def post(self):
        #res = db.GqlQuery('SELECT * FROM Tweet WHERE location =\''+self.request.get('location')+'\' AND category=\''+self.request.get('topic')+'\'')
        res = Tweet.all()
        res.filter("location =", self.request.get('location'))
        res.filter("category =", self.request.get('topic'))
        res.order("time")
        count = res.count();
        result = []
        if(count !=0):
            print '>>>>>>>>>>>>>>>>>>>from datastore'
            for r in res:
                result.append((r.content, r.image, r.username))
        else:
            print "<<<<<<<<<<<<<<<<<<<<<<from Twitter"
            geo = self.getXY(address = self.request.get('location'))
            result = self.searchTweets(self.request.get('topic'), geo)
        for r in result:
            tweet = Tweet(location = self.request.get('location'), category = self.request.get('topic'), content = r[0], image = r[1], username = r[2])
            tweet.put()
        #for i in range(0, len(result)):
        #    print result[i][0], result[i][1], result[i][2]
        results = {'tweets': result}
    	self.response.out.write(template.render('main.html',results))
        
    def getXY(self, address):
        coordinate = urllib.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address="+address+"&sensor=true")
        dict = json.loads(coordinate.read())
        for result in dict["results"]: # result is a list of dictionaries 
            print("*",result["geometry"]["location"]["lat"],"\n")
            print("*",result["geometry"]["location"]["lng"],"\n")
            x=result["geometry"]["location"]["lat"]
            y=result["geometry"]["location"]["lng"]
            break
        return (str(x), str(y));

    def searchTweets(self, category, geocode):
        urlBase = "http://search.twitter.com/search.json?q="
        # construct search URL
        url = urlBase + category + "&geocode=" + geocode[0] + "," + geocode[1] + ",10km&rpp=100"
        search = urllib.urlopen(url)
        # print url, "\n"
        dict = json.loads(search.read())
        ret = []    
        for result in dict["results"]:
            #print "*", result["text"], "\n"
            ret.append((result["text"], result["profile_image_url"], result["from_user"]))
        return ret

class Guestbook(webapp2.RequestHandler):
    def post(self):
        self.response.out.write('<html><body>You wrote:<pre>')
        self.response.out.write(cgi.escape(self.request.get('content')))
        self.response.out.write('</pre></body></html>')

app = webapp2.WSGIApplication([('/', MainPage),
                              ('/sign', Guestbook)],
                              debug=True)
