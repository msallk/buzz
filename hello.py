import cgi
import webapp2

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
    	self.redirect('/');


class Guestbook(webapp2.RequestHandler):
    def post(self):
        self.response.out.write('<html><body>You wrote:<pre>')
        self.response.out.write(cgi.escape(self.request.get('content')))
        self.response.out.write('</pre></body></html>')

app = webapp2.WSGIApplication([('/', MainPage),
                              ('/sign', Guestbook)],
                              debug=True)
