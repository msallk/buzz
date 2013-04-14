import operator
import re

class BuzzExtractor:
	blackList = {	"a",
			"able",
			"about",
			"after",
			"against",
			"again",
			"above",
			"according",
			"accordingly",
			"across",
			"actually",
			"after",
			"afterwards",
			"again",
			"against",
			"aint",
			"all",
			"allow",
			"allows",
			"almost",
			"alone",
			"along",
			"already",
			"also",
			"although",
			"always",
			"am",
			"among",
			"amongst",
			"an",
			"and",
			"another",
			"any",
			"anybody",
			"anyhow",
			"anyone",
			"anything",
			"anyway",
			"anyways",
			"anywhere",
			"apart",
			"appear",
			"appreciate",
			"appropriate",
			"are",
			"arent",
			"around",
			"as",
			"aside",
			"ask",
			"asking",
			"associated",
			"at",
			"available",
			"away",
			"awfully",
			"be",
			"became",
			"because",
			"become",
			"becomes",
			"becoming",
			"been",
			"before",
			"beforehand",
			"behind",
			"being",
			"believe",
			"below",
			"beside",
			"besides",
			"better",
			"between",
			"beyond",
			"both",
			"brief",
			"but",
			"by",
			"cmon",
			"cs",
			"came",
			"can",
			"cant",
			"cannot",
			"cant",
			"cause",
			"causes",
			"certain",
			"certainly",
			"changes",
			"clearly",
			"co",
			"com",
			"come",
			"comes",
			"concerning",
			"consequently",
			"consider",
			"considering",
			"contain",
			"containing",
			"contains",
			"corresponding",
			"could",
			"couldnt",
			"course",
			"currently",
			"definitely",
			"described",
			"despite",
			"did",
			"didnt",
			"different",
			"do",
			"does",
			"doesnt",
			"doing",
			"dont",
			"done",
			"down",
			"downwards",
			"during",
			"each",
			"edu",
			"eg",
			"eight",
			"either",
			"else",
			"elsewhere",
			"en",
			"enough",
			"entirely",
			"especially",
			"et",
			"etc",
			"even",
			"ever",
			"every",
			"everybody",
			"everyone",
			"everything",
			"everywhere",
			"ex",
			"exactly",
			"example",
			"except",
			"far",
			"few",
			"fifth",
			"first",
			"five",
			"followed",
			"following",
			"follows",
			"for",
			"former",
			"formerly",
			"forth",
			"four",
			"from",
			"further",
			"furthermore",
			"get",
			"gets",
			"getting",
			"given",
			"gives",
			"go",
			"goes",
			"going",
			"gone",
			"got",
			"gotten",
			"greetings",
			"had",
			"hadnt",
			"happens",
			"hardly",
			"has",
			"hasnt",
			"have",
			"havent",
			"having",
			"he",
			"hes",
			"hello",
			"help",
			"hence",
			"her",
			"here",
			"heres",
			"hereafter",
			"hereby",
			"herein",
			"hereupon",
			"hers",
			"herself",
			"hi",
			"him",
			"himself",
			"his",
			"hither",
			"hopefully",
			"how",
			"howbeit",
			"however",
			"i",
			"id",
			"ill",
			"im",
			"ive",
			"ie",
			"if",
			"ignored",
			"immediate",
			"in",
			"inasmuch",
			"inc",
			"indeed",
			"indicate",
			"indicated",
			"indicates",
			"inner",
			"insofar",
			"instead",
			"into",
			"inward",
			"is",
			"isnt",
			"it",
			"itd",
			"itll",
			"its",
			"its",
			"itself",
			"just",
			"keep",
			"keeps",
			"kept",
			"know",
			"knows",
			"known",
			"last",
			"lately",
			"later",
			"latter",
			"latterly",
			"least",
			"less",
			"lest",
			"let",
			"lets",
			"like",
			"liked",
			"likely",
			"little",
			"lol",
			"look",
			"looking",
			"looks",
			"ltd",
			"mainly",
			"many",
			"may",
			"maybe",
			"me",
			"mean",
			"meanwhile",
			"merely",
			"might",
			"more",
			"moreover",
			"most",
			"mostly",
			"much",
			"must",
			"my",
			"myself",
			"name",
			"namely",
			"nd",
			"nearly",
			"necessary",
			"need",
			"needs",
			"neither",
			"never",
			"nevertheless",
			"new",
			"next",
			"nine",
			"no",
			"nobody",
			"non",
			"none",
			"noone",
			"nor",
			"normally",
			"not",
			"nothing",
			"novel",
			"now",
			"nowhere",
			"obviously",
			"of",
			"off",
			"often",
			"oh",
			"ok",
			"okay",
			"old",
			"on",
			"or",
			"once",
			"one",
			"ones",
			"only",
			"onto",
			"other",
			"others",
			"otherwise",
			"ought",
			"our",
			"ours",
			"ourselves",
			"out",
			"outside",
			"over",
			"overall",
			"own",
			"particular",
			"particularly",
			"per",
			"perhaps",
			"placed",
			"please",
			"plus",
			"possible",
			"presumably",
			"probably",
			"provides",
			"que",
			"quite",
			"qv",
			"rather",
			"rd",
			"re",
			"really",
			"reasonably",
			"regarding",
			"regardless",
			"regards",
			"require",
			"requires",
			"relatively",
			"respectively",
			"right",
			"rt",
			"said",
			"same",
			"saw",
			"say",
			"saying",
			"says",
			"second",
			"secondly",
			"see",
			"seeing",
			"seem",
			"seemed",
			"seeming",
			"seems",
			"seen",
			"self",
			"selves",
			"sensible",
			"sent",
			"serious",
			"seriously",
			"seven",
			"several",
			"shall",
			"she",
			"should",
			"shouldnt",
			"since",
			"six",
			"so",
			"some",
			"somebody",
			"somehow",
			"someone",
			"something",
			"sometime",
			"sometimes",
			"somewhat",
			"somewhere",
			"soon",
			"sorry",
			"specified",
			"specify",
			"specifying",
			"still",
			"sub",
			"such",
			"sup",
			"sure",
			"ts",
			"take",
			"taken",
			"tell",
			"tends",
			"th",
			"than",
			"thank",
			"thanks",
			"thanx",
			"that",
			"thats",
			"thats",
			"the",
			"their",
			"theirs",
			"them",
			"themselves",
			"then",
			"thence",
			"there",
			"theres",
			"thereafter",
			"thereby",
			"therefore",
			"therein",
			"theres",
			"thereupon",
			"these",
			"they",
			"theyd",
			"theyll",
			"theyre",
			"theyve",
			"think",
			"third",
			"this",
			"thorough",
			"thoroughly",
			"those",
			"though",
			"three",
			"through",
			"throughout",
			"thru",
			"thus",
			"together",
			"to",
			"too",
			"took",
			"toward",
			"towards",
			"tried",
			"tries",
			"truly",
			"try",
			"trying",
			"twice",
			"twitter",
			"twitpic",
			"under",
			"unfortunately",
			"unless",
			"unlikely",
			"unto",
			"up",
			"upon",
			"us",
			"use",
			"used",
			"useful",
			"uses",
			"using",
			"usually",
			"value",
			"various",
			"very",
			"via",
			"viz",
			"vs",
			"want",
			"wants",
			"was",
			"wasnt",
			"way",
			"we",
			"wed",
			"well",
			"were",
			"weve",
			"welcome",
			"well",
			"went",
			"were",
			"werent",
			"what",
			"whats",
			"whatever",
			"when",
			"whence",
			"whenever",
			"where",
			"wheres",
			"whereafter",
			"whereas",
			"whereby",
			"wherein",
			"whereupon",
			"wherever",
			"whether",
			"which",
			"while",
			"whither",
			"who",
			"whos",
			"whoever",
			"whole",
			"whom",
			"whose",
			"why",
			"will",
			"willing",
			"wish",
			"with",
			"without",
			"wont",
			"wonder",
			"would",
			"would",
			"wouldnt",
			"yes",
			"yet",
			"you",
			"youd",
			"youll",
			"youre",
			"youve",
			"your",
			"yours",
			"yourself",
			"yourselves",
			"rt",
			"ht",
			"oh",
			"ff",
			"de",
			"",
			" "
		}

	wordList = {}

	# the function need to be called
	# pass the tweets list from tweetor API
	# return a list of pairs, which consists of buzz and tweets associated with this buzz
	def getCategorizedTweets(self, tweetList):
		self.putTweets(tweetList)
		#for word in self.wordList:
		#	print word
		buzzes = self.getPopularBuzz()
		#for buzz in buzzes:
		#	print buzz
		return self.categorizeTweet(buzzes, tweetList)
		#self.printTweet(self.categorizeTweet(buzzes, tweetList))

	def putTweets(self, tweetList):
		for tweet in tweetList:
			#print tweet[0]
			self.putWords(tweet[1].lower())

	def getPopularBuzz(self):
		sortList = sorted(self.wordList.iteritems(), key=operator.itemgetter(1))
		sortList.reverse()
		if len(sortList) < 10:
			bound = len(sortList)
		else:
			bound = 10;

		ret = []
		for i in range(0, bound):
			ret.append(sortList[i][0])
		return ret

	# how to split a tweet
	# need refine
	def splitTweet(self, tweet):
		words = tweet.split()
		pattern = re.compile('[\W]', re.UNICODE)
		for it in range(0, len(words)):
			words[it] = str(pattern.sub('', words[it]))
		return words

	def putWords(self, tweet):
		words = self.splitTweet(tweet)
		for word in words:
			#print word
			if len(word) <= 1:
				continue
			if word in self.blackList:
				continue
			if word.startswith("http"):
				continue

			if word in self.wordList:
				self.wordList[word] = self.wordList[word] + 1
			else:
				self.wordList[word] = 1

	# for debug
	def printTweet(self, retList):
		for pair in retList:
			print '\n------------'
			print pair[0]

			for item in pair[1]:
				print '\t*', item[0], item[1], item[2], item[3]


	def categorizeTweet(self, buzzes, tweetList):
		#get a empty ret list
		ret = []
		for buzz in buzzes:
			ret.append((buzz, []));

		#check each tweet with every buzz
		for tweet in tweetList:
			for pair in ret:
				if self.belongToBuzz(pair[0],tweet[1].lower()):
					pair[1].append(tweet)
		return ret

	def belongToBuzz(self, buzz, tweet):
		words = self.splitTweet(tweet)
		for word in words:
			if buzz == word:
				return True
		return False

#test part
#b = BuzzExtractor()
#str = ("A dictionary in Python can be directly looped over with a for-loop", "A Python dictionary may or may not contain a specific key")
#b.putTweets(str)
