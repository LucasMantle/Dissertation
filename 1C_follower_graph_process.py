import tweepy
import numpy as np
import itertools

# Consumer
consumer_key = 'ZpXvAS4t6IjrWcOigQwl9rVTt'
consumer_secret = '33oowDZ8udR3piqJ1fPza45jl1zwMfpcVVmVQrRtOqoGYOV2SO'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Access
access_key = '1403340536094892035-ZXx7QaleDtxbiDf6nZAghQlsLtiXmm'
access_secret = 'HS5hJBmsdnhespyEJR7ffmjqCPzrTBiyCAbcCVJ2fHLp9'
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user_list = []
with open('Users&Keywords/checked_users.txt', 'r') as users:
    Lines = users.readlines()
    for line1 in Lines:
        source = line1.strip()
        user_list.append(source)

follower_graph = {user: {user2: 0 if user != user2 else 1 for user2 in user_list} for user in user_list}
combinations = [comb for comb in itertools.combinations(user_list, 2)]

print(combinations)

for source, target in combinations:
    print(source, target, '----')
    friendship = api.show_friendship(source_screen_name=source, target_screen_name=target)
    ## Source follows target
    if friendship[0].following:
        follower_graph[source][target] = 1
    # Target follows source
    if friendship[0].followed_by:
        follower_graph[target][source] = 1

follower_graph_array = np.empty((len(user_list), len(user_list)))
for source, count1 in zip(user_list, range(len(user_list))):
    for target, count2 in zip(user_list, range(len(user_list))):
        follower_graph_array[count1][count2] = follower_graph[source][target]

print('Follower Graph has been generated and saved')
np.savetxt('Data/DataPrior/Follower_Graph.txt', follower_graph_array, fmt='%d')

