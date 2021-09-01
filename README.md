# Dissertation 

This repo provides all the code and relevant files used within 
my MSc Data Science Dissertation

Breaking down all relevant files: 

    Users&Keywords:
    
        Users: 
            This file contains all the twitter handles of the users 
            that tweets were scraped from
        Keywords: 
            This file contains the keywords used to search tweets. 
     
    Data: 
    
        Data contains all the data used within the thesis. 
        It is the data scraped from twitter using the users and keywords files. 
        
    
    .py Files: 
    
        All the .py files are in the form #*_*.py or _#*_.py, where # indicates
        a number and * indicates a letter or word. 
        
        #*_*.py files are the main files which are used and directly ran, while
        _#*_*.py files are functions which are imported in their respective 
        main files.
        
        The numbers in these file names refer to a part in the modelling pipeline. 
        Specifically, parts 1-4 deal with the collecting, preprocessing and
        wrangling of the data. Parts 5 and 6 do the tuning of ANNs and LSTMs, 
        respectively. Part 7 just outputs the obtained results.
        
        Part 8_runner.py provides a python file to run multiple .py files at once. 
        
        The order of the .py are as follows:
        
        0_clear_dir.py
        1_collection.py
        1_collection_test.py
        1A_tweet_data_collection_process.py
        1B_user_checker.py
        1C_follower_graph_process.py
        2_distributions.py
        3A_with_fg.py
        3A_without_fg.py
        4_cleaning.py
        5_tuning.py
        6_tuning.py
        7_results.py
        
    requirements.txt: 
        
        This provides the librarires used. 'pip install -r requirements.txt' will
        install all required libraries. You may need to install twint separately.
        This can be done by cloning their github.

In-order to run the code end-to-end, 8_runner.py can be run. You need to 
edit (uncomment) the specific files you want to run. 

If you would like to adjust the dates of tweet scraping, these can be found
in both 1_collection.py and 1_collection_test.py

There may be some issues when running some files as they require different 
versions of pandas and numpy. 
To solve this issue, from parts 0-5, uninstall pandas and numpy and install them - 
this should get the latest versions.
However, when running part 6, run 'pip install numpy==1.19.5'. 

The best way to run this code is run files 0-4, ensuring
all libraries dependencies have been modified (mentioned above). This will
ensure all the data is collected, processed and wrangled. 
Then running parts 5 and 6 separately will tune the models for each type 
of data input. Running part 7 will output the results obtained. 
