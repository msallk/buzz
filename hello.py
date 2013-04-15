import cgi
import webapp2
import urllib
import json
import time
import sys
import buzzExtractor
import SentimentAnalysis

from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Tweet(db.Model):
    location = db.StringProperty(required = True)
    category = db.StringProperty(required = True)
    user = db.StringProperty(required = False)
    content = db.StringProperty(required = False, multiline = True)
    image = db.StringProperty(required = False)
    username = db.StringProperty(required = False)
    time = db.DateTimeProperty(auto_now_add = True)



class MainPage(webapp2.RequestHandler):
    def get(self):
    	res = []
        result = []
        for r in res:
            result.append((r.content, r.image, r.username))
    	results = {'tweets': result}
        self.response.out.write(template.render('main.html', results))
    def post(self):
        #res = db.GqlQuery('SELECT * FROM Tweet WHERE location =\''+self.request.get('location')+'\' AND category=\''+self.request.get('topic')+'\'')
        #self.clearDatastore()
        res = Tweet.all()
        res.filter("location =", self.request.get('location'))
        res.filter("category =", self.request.get('topic'))
        res.order("time")
        count = res.count();
        result = []
        if(count !=0):
            print '>>>>>>>>>>>>>>>>>>>from datastore'
            for r in res:
                result.append((r.user, r.content, r.image, r.username))
        else:
            print "<<<<<<<<<<<<<<<<<<<<<<from Twitter"
            geo = self.getXY(address = self.request.get('location'))
            result = self.searchTweets(self.request.get('topic'), geo)
            for r in result:
                tweet = Tweet(location = self.request.get('location'), category = self.request.get('topic'), user = r[0], content = r[1], image = r[2], username = r[3])
                tweet.put()
        #for i in range(0, len(result)):
        #    print result[i][0], result[i][1], result[i][2]
        buzz = []
        categorized = []
        categorized2 = []
        results = []
        buzz = buzzExtractor.BuzzExtractor()
        categorized = buzz.getCategorizedTweets(result)
        sAnalyzer = SentimentAnalysis.Analyzer()
        categorized2 = sAnalyzer.analyze(categorized)
        results = {'tweets': categorized2}
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
        # construct search URL
        url = "http://search.twitter.com/search.json?q=" + category + "&geocode=" + geocode[0] + "," + geocode[1] + ",10km&rpp=100"
        search = urllib.urlopen(url)
        # print url, "\n"
        dict = json.loads(search.read())
        ret = []
        for result in dict["results"]:
            #print "*", result["text"], "\n"
            ret.append((result["from_user"], result["text"], result["profile_image_url"], result["from_user_name"]))
        return ret

    def clearDatastore(self):
        db.delete(db.Query())

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
