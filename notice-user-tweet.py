from requests_oauthlib import OAuth1Session
import requests
import datetime
import json
import pandas as pd
import sys
import os
import time
nbm = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '') # non_bmp_map
import re

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
params ={'user_id' : sys.argv[1]}

csv_path = "%s/csv/%s.csv" % (os.path.dirname(os.path.abspath(__file__)), sys.argv[1])
csv_charset = "utf-8"

webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def pushToDiscord(sname,tweetid,icon):
    main_content = {
      "content": "https://twitter.com/%s/status/%s" % (sname, tweetid),
      "avatar_url": icon
    }
    requests.post(webhook_url, main_content)

def get_tweets():
    # OAuth
    twitter = OAuth1Session(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    time.sleep(1)
    req = twitter.get(url, params = params)
    arr = []

    if req.status_code == 200:
        timeline = json.loads(req.text)
        for status in timeline:
            time1 = str(status["created_at"])
            time2 = datetime.datetime.strptime(status["created_at"], "%a %b %d %H:%M:%S %z %Y")
            time2 = (time2 + datetime.timedelta(hours=9)).strftime("%Y/%m/%d %H:%M:%S")
            tweetid = str(status["id"])
            userid = str(status["user"]["id"])
            name = status["user"]["name"].translate(nbm)
            sname = status["user"]["screen_name"].translate(nbm)
            source = cleanhtml(status["source"])
            text = status["text"].translate(nbm)
            geo = status["geo"]
            coordinates = status["coordinates"]
            place = status["place"]

            userloc = status["user"]["location"]
            userdes = status["user"]["description"]
            userurl = status["user"]["url"]
            userprotect = status["user"]["protected"]
            followers = status["user"]["followers_count"]
            follows = status["user"]["friends_count"]
            lists = status["user"]["listed_count"]
            created_at = status["user"]["created_at"]
            favourites = status["user"]["favourites_count"]
            tweets_counts = status["user"]["statuses_count"]
            profile_image = status["user"]["profile_image_url_https"]
            profile_background = status["user"]["profile_use_background_image"]

            arrrr = [time1, time2, tweetid, userid, name, sname, source, text, geo, coordinates, place, userloc, userdes, userurl, userprotect, followers, follows, lists, created_at, favourites, tweets_counts, profile_image, profile_background]
            arr.append(arrrr)
            
            time2c = datetime.datetime.strptime(time2, "%Y/%m/%d %H:%M:%S")
            dt_now = datetime.datetime.now()
            if dt_now - time2c < datetime.timedelta(minutes = 0,seconds = 6):
                pushToDiscord(sname,tweetid,profile_image)

    else:
        print("ERROR: %d" % req.status_code)
    
    arr.reverse()
    return(arr)


def main():
    arr = get_tweets()
    df = pd.DataFrame(arr, columns=['time','localTime','tweetId','userId','screenName','userName','source','text', 'geo', 'coordinates', 'place', 'userloc', 'userdes', 'userurl', 'userprotect', 'followers', 'follows', 'lists', 'created_at', 'favourites', 'tweets_counts','profile_image', 'profile_background'])

    if not os.path.exists(csv_path):
        df.to_csv(csv_path, encoding=csv_charset, index=None)
    else:
        df_0 = pd.read_csv(csv_path, encoding=csv_charset)
        df_out = pd.concat([df_0, df])
        df_out = df_out.drop_duplicates(['tweetId'])
        df_out.to_csv(csv_path, encoding=csv_charset, index=None)

if __name__ == "__main__":
    main()
    endtime = datetime.datetime.now()
    print('%s done' % endtime)
