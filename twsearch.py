#!/usr/bin/env python3

import re
import sys
from twython     import Twython
from collections import Counter
from nltk.corpus import stopwords


def tags(hashtags):
    if len(hashtags) > 0:
        return [hashtag['text'] for hashtag in hashtags]
    else:
        return []


def simplify_text(text):
    """ Removes some noise from a given Twitter text """

    # Remove links:
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    for char in ['#', '@',
                 '.', ',', ';', ':',
                 '?', '!', '%', '$',
                 '*', '+', '/', '(', ')', '[', ']', "'", '"']:
        text = text.replace(char, '')

    text = text.lower()

    return text


def tokenize_text(text): return text.split()


def only_meaningful(words):
    return [word
            for word in words
            if word not in stop_words]

stop_words = set(stopwords.words('english'))


TWITTER_APP_KEY = sys.argv[1]
TWITTER_APP_KEY_SECRET = sys.argv[2]
TWITTER_ACCESS_TOKEN = sys.argv[3]
TWITTER_ACCESS_TOKEN_SECRET = sys.argv[4]

t = Twython(app_key=TWITTER_APP_KEY,
            app_secret=TWITTER_APP_KEY_SECRET,
            oauth_token=TWITTER_ACCESS_TOKEN,
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

search = t.search(q='#ethereum',
                  count=100)

tweets = search['statuses']

# for tweet in tweets:
#     tags_list = tags(tweet['entities']['hashtags'])
#     words = tokenize_text(simplify_text(tweet['text']))
#     meaningful_words = only_meaningful(words)
#     print(tweet['id'], tweet['created_at'], tags_list, meaningful_words)

def bundle_tweets(tweets):
    """ Bundles all the text in the tweets into a single string """

    result = ''

    for tweet in tweets:
        result += tweet['text']

    return result


all_tweets = bundle_tweets(tweets)
words = tokenize_text(simplify_text(all_tweets))
meaningful_words = only_meaningful(words)

counts = Counter(meaningful_words)

for word, count in counts.most_common(100):
    print(word, ' (', count, ' times)')
