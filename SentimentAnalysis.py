
class Analyzer:
	afinn = {}
	def __init__(self):
		self.afinn = dict(map(lambda (k,v): (k,int(v)), 
                     [ line.split('\t') for line in open("AFINN-111.txt") ]))
	def analyze(self, content):
		return sum(map(lambda word: self.afinn.get(word, 0), content.lower().split()))

analyzer = Analyzer()
print analyzer.analyze("Rainy day but still in a good mood")
