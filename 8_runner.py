import os

os.system('python 0_clear_dir.py')
print('Prior data is being scraped')
os.system('python 1_collection.py')
print('Test Data is being Scraped')
os.system('python 1_collection_test.py')
print('All is done')

# os.system('python 1A_tweet_data_collection_process.py')
# print('4')
# os.system('python 1B_user_checker.py')
# print('5')
# os.system('python 1C_follower_graph_process.py')
#
# os.system('python 2_distributions.py')
#
# os.system('python 3A_with_fg.py')
# os.system('python 3A_without_fg.py')
#
# os.system('python 4_cleaning.py')
#
# os.system('python 5_tuning.py')
# os.system('python 6_tuning.py')
#
# os.system('python 7_results.py')


