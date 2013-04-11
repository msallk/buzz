import urllib
import json

urlBase = "http://search.twitter.com/search.json?q="

def searchTweets(category, geocode):
	# construct search URL
	url = urlBase + category + "&geocode=" + geocode[0] + "," + geocode[1] + ",10km"
	search = urllib.urlopen(url)
	# print url, "\n"
	dict = json.loads(search.read())
	ret = []
	for result in dict["results"]:
		#print "*", result["text"], "\n"
		ret.append((result["text"], result["profile_image_url"], result["from_user"]))
	return ret



l = searchTweets("sport", ("37.421401","-122.08537"))
for i in range(0, len(l)):
	print "*", l[i][0], l[i][1], l[i][2]
