import tweepy
import csv
import time
import re
import MeCab
from sudachipy import tokenizer
from sudachipy import dictionary
tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.A

API_Key = ""
API_Secret = ""
Accsess_Token = ""
Accsess_Token_Secret = ""


auth = tweepy.OAuthHandler(API_Key, API_Secret)
auth.set_access_token(Accsess_Token, Accsess_Token_Secret)
api = tweepy.API(auth)
max_tweets = 20000
# 131kb


def getMtTweet():
    tweets = []
    num = 0
    i = 1
    print('page ' + str(i))
    tweet_data = api.user_timeline(screen_name="Jasper7se", count=100)

    if len(tweet_data) > 0:
        for tweet in tweet_data:
            content = re.sub(
                r"^@.+\s|\"|\n|https?://[\w/:%#\$&\?\(\)~\.=\+\-]+|#.*", "", tweet.text)

            if content.startswith("RT @"):
                continue

            tweets.append([content])
            num += 1
        i += 1
        next_max_id = tweet_data[-1].id

        while True:

            print('page ' + str(i))
            tweet_data = api.user_timeline(
                screen_name="jasper7se", count=100, max_id=next_max_id-1)

            if len(tweet_data) > 0:
                next_max_id = tweet_data[-1].id
                for tweet in tweet_data:
                    content = re.sub(
                        r"@.+\s|\"|\n|https?://[\w/:%#\$&\?\(\)~\.=\+\-]+|#.*", "", tweet.text)

                    if content.startswith("RT @"):
                        continue

                    tweets.append([content])
                    num += 1
                if num >= max_tweets:
                    break
                i += 1
                time.sleep((15*60)/180)
            else:
                break
            saveTweets(tweets)


def saveTweets(tweets):
    file_path = './data/Tweets.txt'
    file = open(file_path, 'w', encoding='UTF-8')
    m = MeCab.Tagger('-Owakati')

    table = str.maketrans({
        '\n': '',
        '\r': '',
        '(': '（',
        ')': '）',
        '[': '［',
        ']': '］',
        '"': '”',
        "'": "’",
    })

    for text in tweets:
        t = text[0].translate(table).split()
        try:
            split_text = [m.surface()
                          for m in tokenizer_obj.tokenize(t[0], mode)]
        except:
            pass

        file.write(" ".join(split_text)+"\n")
    file.close()

    with open(file_path, encoding='utf-8') as f:
        print(f.read())


if __name__ == '__main__':
    getMtTweet()
