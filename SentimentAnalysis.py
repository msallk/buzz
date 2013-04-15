
class Analyzer:
	afinn = {}
	def __init__(self):
		self.afinn = dict(map(lambda (k,v): (k,int(v)), 
                     [ line.split('\t') for line in open("AFINN-111.txt") ]))
	def analyzeTweet(self, content):
		return sum(map(lambda word: self.afinn.get(word, 0), content.lower().split()))
	def analyzeList(self, tweets):
		count = 0
		sent = "Neutral"
		for tweet in tweets:
			count += self.analyzeTweet(tweet[1])
		if count > 8:
			sent = "Positive"
		if count < -8:
			sent = "Negative"
		if count > 25:
			sent = "Very Positive"
		if count < -25:
			sent = "Very Negative"
		return sent
	def analyze(self, categorizedList):
		for tweets in categorizedList:
			tweets[0] = (tweets[0], self.analyzeList(tweets[1]))
			print ".......................", self.analyzeList(tweets[1])
		return categorizedList

analyzer = Analyzer()
print analyzer.analyzeTweet("Rainy day but still in a good mood")