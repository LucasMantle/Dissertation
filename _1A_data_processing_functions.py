# Removes any URLS
def remove_url(x):
    import re
    return re.sub(r'http\S+', '', x)


# Puts time in the format wanted
def fix_date(x):
    from datetime import datetime
    return datetime.strptime(x[:18], '%Y-%m-%d %H:%M:%S')


# Gathers timezone
def date_timezone(x):
    return x[20:]


# def remove_ats(x):
#     import re
#     return re.sub('@[\w]+', '', x)

# Removes @'s
def remove_ats(x):
    import re
    return re.sub('@[^\s]+', '', x)


# Removes hashtags
def remove_hash(x):
    import re
    return re.sub('#', '', x)


# Swaps amp to &
def swap_amp(x):
    return x.replace('&amp;', '&')


# Determines tense
def determine_tense_input(sentence):
    from nltk import word_tokenize, pos_tag
    import nltk
    text = word_tokenize(sentence)
    # Tagging words
    sentence_tagged = pos_tag(text)

    tense = {}

    # Tags refer to specific meanings. Each can be utilised to tag these as past, present or future tense
    tense["future"] = len([word for word in sentence_tagged if word[1] == "MD"])
    tense["present"] = len([word for word in sentence_tagged if word[1] in ["VBP", "VBZ", "VBG"]])
    tense["past"] = len([word for word in sentence_tagged if word[1] in ["VBD", "VBN"]])
    return tense["past"], tense["present"], tense["future"]


# These set of functions make tense columns binary
def past_tense(x):
    if x[0] > 0:
        return 1
    else:
        return 0


def present_tense(x):
    if x[1] > 0:
        return 1
    else:
        return 0


def future_tense(x):
    if x[2] > 0:
        return 1
    else:
        return 0


# Applies all necessary processing functions
def apply_processing(df):
    df['date'] = df['created_at'].apply(fix_date)
    df['time_zone'] = df['created_at'].apply(date_timezone)

    df['tweet'] = df['tweet'].apply(remove_url)
    df['tweet'] = df['tweet'].apply(remove_ats)
    df['tweet'] = df['tweet'].apply(remove_hash)
    df['tweet'] = df['tweet'].apply(swap_amp)

    df['tenses'] = df['tweet'].apply(determine_tense_input)
    df['past_tense'] = df['tenses'].apply(past_tense)
    df['present_tense'] = df['tenses'].apply(present_tense)
    df['future_tense'] = df['tenses'].apply(future_tense)

    return df[['date', 'tweet', 'past_tense', 'present_tense', 'future_tense', 'replies_count', 'retweets_count',
               'likes_count']]
