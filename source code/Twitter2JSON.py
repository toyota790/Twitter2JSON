#*****************************************
#       William Luo  April 9, 2016
# ----------------------------------------
#    Get the Twitter tweet data and
#       output to the JSON file.
#*****************************************
import twitter
import urlparse
import sys
import json
import os
import io
import logging
import time
from datetime import datetime
from pprint import pprint as pp
from collections import namedtuple

class IO_json(object):
	"""docstring for IO_json"""
	def __init__(self, filepath, filename, filesuffix='json'):
		self.filepath = filepath
		self.filename = filename
		self.filesuffix = filesuffix

	def save(self, data):
		if os.path.isfile('{0}/{1}.{2}'.format(self.filepath, self.filename, self.filesuffix)):
			# Append existing file
			with io.open('{0}/{1}.{2}'.format(self.filepath, self.filename, self.filesuffix), 'a', encoding = 'utf-8') as f:
				f.write(unicode(json.dumps(data, ensure_ascii = False)))
		else:
			with io.open('{0}/{1}.{2}'.format(self.filepath, self.filename, self.filesuffix), 'w', encoding = 'utf-8') as f:
				f.write(unicode(json.dumps(data, ensure_ascii = False)))
                
	def load(self):
		with io.open('{0}/{1}.{2}'.format(self.filepath, self.filename, self.filesuffix), encoding = 'utf-8') as f:
			return f.read()	

class TwitterAPI(object):

    def __init__(self):
        consumer_key = 'Your application\'s consumer key'
        consumer_secret = 'Your application\'s consumer secret'
        access_token = 'Your OAuth token'
        access_secret = 'Your OAuth token secret'
     
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret
        self.retries = 3
        self.auth = twitter.oauth.OAuth(access_token, access_secret, consumer_key, consumer_secret)
        self.api = twitter.Twitter(auth=self.auth)

        #logger initialisation
        appName = 'TwitterOutput'
        self.logger = logging.getLogger(appName)
        #create console handler and set level to debug
        logPath = '/home/william/Python/Twitter/Log'
        
        fileName = appName
        fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(logging.DEBUG)
        
        #Save to JSON file initialisation
        jsonFpath = '/home/william/Python/Twitter/Data/JSON'
        jsonFname = 'TwitterOutput'
        self.jsonSaver = IO_json(jsonFpath, jsonFname)

    def searchTwitter(self, q, max_res=10,**kwargs):
        search_results = self.api.search.tweets(q=q, count=10, **kwargs)
        statuses = search_results['statuses']
        max_results = min(1000, max_res)

        for _ in range(10): 
            try:
                next_results = search_results['search_metadata']['next_results']
            except KeyError as e: 
                break

            next_results = urlparse.parse_qsl(next_results[1:])
            kwargs = dict(next_results)
            search_results = self.api.search.tweets(**kwargs)
            statuses += search_results['statuses']
            self.saveTweets(search_results['statuses'])

            if len(statuses) > max_results: 
                self.logger.info('info in searchTwitter - got %i tweets - max: %i' %(len(statuses), max_results))
                pp('info in searchTwitter - got %i tweets - max: %i' %(len(statuses), max_results))
                break
        return statuses

    def saveTweets(self, statuses):
    	# Saving to JSON File
    	self.jsonSaver.save(statuses)

    def parseTweets(self, statuses):
    	# Allow us to extract the key tweet information from the vast amaount of information
        return [ (status['id'], 
                  status['created_at'], 
                  status['user']['id'],
                  status['user']['name'], 
                  status['text'], 
                  url['expanded_url']) 
                        for status in statuses 
                            for url in status['entities']['urls']]

    def getTweets(self, q, max_res=10):
        #Make a Twitter API call whilst managing rate limit and errors.

        def handleError(e, wait_period=2, sleep_when_rate_limited=True):
            if wait_period > 3600:
                self.logger.error('Too many retries in getTweets: %s', e)
                raise e
            if e.e.code == 401:
                self.logger.error('error 401 * Not Authorised * in getTweets: %s', e)
                return None
            elif e.e.code == 404:
                self.logger.error('error 404 * Not Found * in getTweets: %s', e)
                return None
            elif e.e.code == 429:
                self.logger.error('error 429 * API Rate Limit Exceeded * in getTweets: %s', e)
                if sleep_when_rate_limited:
                    self.logger.error('error 429 * Retrying in 15 minutes * in getTweets: %s', e)
                    sys.stderr.flush()
                    time.sleep(60*15 + 5)
                    self.logger.info('error 429 * Retrying now * in getTweets: %s', e)
                    return 2
                else:
                    raise e
            elif e.e.code in (500, 502, 503, 504):
                self.logger.info('Encountered %i Error. Retrying in %i seconds', e.e.code, wait_period)
                time.sleep(wait_period)
                wait_period *= 1.5
                return wait_period
            else:
                self.logger.error('Exit - aborting - %s', e)
                raise e
        while True:
            try:
                tsearch = self.searchTwitter(q, max_res=10)
                tparsed = t.parseTweets(tsearch)
            except twitter.api.TwitterHTTPError as e:
                wait_period = 2
                error_count = 0
                wait_period = handleError(e, wait_period)
                if wait_period is None:
                    return
t = TwitterAPI()
#Query keyword
q = "#panamapapers"
t.getTweets(q, 10)
