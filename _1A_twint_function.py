import twint
import os


def collect_tweets(since, until, use_keywords=True):
    with open("Users&Keywords/keywords.txt", "r") as keywords:
        words = keywords.readline().strip()
        for l in keywords.readlines():
            words += ' OR ' + l.strip()

    c = twint.Config()
    c.Since = since
    c.Until = until
    #     "2019-01-01"

    c.Custom["tweet"] = ["id", "username", "created_at", "timezone", "user_id", "tweet", "mentions", "urls",
                         "replies_count", "retweets_count", "likes_count", "hashtags", "retweet", "source"]
    if use_keywords:
        c.Search = words
    c.Store_csv = True
    c.Lang = 'en'
    c.Hide_output = True

    with open('Users&Keywords/users.txt', 'r') as users:
        Lines = users.readlines()
        for line in Lines:
            c.Username = line.strip()

            # Clear existing CSV
            if not use_keywords:
                csv_name = "Data/DataPrior/Raw/" + line.strip().lower() + ".csv"
            else:
                csv_name = "Data/DataTest/Raw/" + line.strip().lower() + ".csv"

            try:
                os.remove(csv_name)
            except:
                pass
            c.Output = csv_name
            try:
                twint.run.Search(c)
            except:
                continue
