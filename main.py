import markovify
import MeCab
import get_tweet
import emoji
import tweepy

auth = tweepy.OAuthHandler(get_tweet.API_Key, get_tweet.API_Secret)
auth.set_access_token(get_tweet.Accsess_Token, get_tweet.Accsess_Token_Secret)
api = tweepy.API(auth)





def main():
    file = open("./data/Tweets.txt", "r", encoding="utf-8").read()
    sentence = None

    while sentence is None:
        text_model = markovify.NewlineText(file, state_size=2)
        sentence = text_model.make_short_sentence(140)
        sentence = "".join(sentence.split())
        print(sentence)

    with open('./data/learned_data.json', 'w') as f:
        f.write(text_model.to_json())


if __name__ == '__main__':
    main()
