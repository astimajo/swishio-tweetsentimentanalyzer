import csv, tweepy, os
from textblob import TextBlob
import new_file 

class Conn:
    '''
        twitter credentials class
    '''
    def __init__(self, *args):
        self.ck = 'fUEl1vqhD3FO37I12c0mXfQpo'                             #consumer key
        self.cs = 'THQXyMK5YZQ66sGPizhM3tFOCETRhQg8Rm1AChPOQGntMo5A1g'    #consumer secret
        self.at = '1149663947676479488-Fj02BUZShgRBJbPkkw2hFHKj4BvRmk'    #access token
        self.ats = 'FsUFTot9IaDRPmGPmO4jPsStMSKJT8dv980GgfatOW1k3'        #access token secret
    
    def tweep_creds(self):
        auth = tweepy.OAuthHandler(self.ck, self.cs)
        auth.set_access_token(self.at, self.ats)
        return tweepy.API(auth, wait_on_rate_limit=True)

#initialize api w/ twitter api credentials object
api = Conn().tweep_creds()

#function to add language to csv row
def add_language(query_word, twt_lmt):
    for tweet in list(tweepy.Cursor(api.search, q=query_word).items(twt_lmt)):
        
        tweet = TextBlob(tweet.text)
        
        language = tweet.detect_language()

    return language

#function to gather polarity of a specific tweet to estimate sentiments
def add_sentiment(query_word,twt_lmt):
    for tweet in list(tweepy.Cursor(api.search, q=query_word).items(twt_lmt)):
        
        tweet = TextBlob(tweet.text)
        
        if tweet.sentiment.polarity > 0:
            sentiment = str("Positive Tweet")

        elif tweet.sentiment.polarity < 0:
            sentiment = str("Negative Tweet")

        else:
            sentiment = str("Neutral Tweet")

    return sentiment

# gather tweets using the initialized twitter api. 
def gather_tweets_sentiments(query_word,twt_lmt, sentiment, language):
    counter = 0
    for tweet in list(tweepy.Cursor(api.search, q=query_word).items(twt_lmt)):
        csvWriter.writerow([tweet.text, tweet.user.screen_name, tweet.created_at, tweet.user.location, tweet.retweet_count, tweet.favorite_count, sentiment, language])
        counter = counter + 1
    return counter


# tweet filename
global csvWriter
new_file.create_file()
namefile = "tweets.csv"
dir_name = os.path.dirname(os.path.abspath(__file__))
file_dir = open(dir_name+"/"+namefile,'r', encoding='ISO-8859-1')
csvFile = open(dir_name+"/"+namefile,'a')
csvreader = csv.reader(file_dir)
csvWriter = csv.writer(csvFile)
row_cnt = sum(1 for row in file_dir)


q_words = "duterte" # enter query words here (separate by spaces)
q_words = q_words.split()

t_lmt = tweet_limit = 15 #adjust tweet limit accordingly
limit_num = tweet_limit * len(q_words)
new_rc = row_cnt

for q in q_words:
    new_rc += gather_tweets_sentiments(q, t_lmt, add_sentiment(q, t_lmt), add_language(q, t_lmt))


print("initial rows: %s\ngathered rows: %s"%(row_cnt,new_rc-row_cnt))
csvFile.close()