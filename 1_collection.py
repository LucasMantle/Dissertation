import _1A_twint_function

# These dates outline the days which are collected for prior and testing data
# y-m-d
data_since = "2017-01-01"
# Where to split prior data and current data
split_date_prior = '2018-04-01 00:00:00'
test_start_date = '2018-04-02 00:00:00'
end_date = '2021-08-01 00:00:00'

# Run tweet collection
# Data has been stored in TweetData as **user**.csv
# Getting prior data - we dont need keyword search as this is just prior general sentiment
_1A_twint_function.collect_tweets(data_since, split_date_prior, use_keywords=False)

# Getting testing data where we want to compare sentiment to specific market
# _1A_twint_function.collect_tweets(split_date_prior, end_date, use_keywords=True)
