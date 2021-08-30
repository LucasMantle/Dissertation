# Dissertation 

This repo provides all the code and relevant files used within 
my MSc Data Science Dissertation

Breaking down relevant files: 

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
        
        The numbers refer a given part which are mentioned below to go through
        how to run the code.

In-order to run the code end-to-end, 8_runner.py can be run. You need to 
edit (uncomment) the specific files you want to run. 

If you would like to adjust the dates of tweet scraping, these can be found
in both 1_collection.py and 1_collection_test.py

There may be some issues when running some files as they require different 
versions of pandas and numpy. 
To solve this issue, from parts 0-5, uninstall pandas and numpy and install them - 
this should get the latest versions.
However, when running part 6, run 'pip install numpy==1.19.5'. 

The best way to run this code is to uncomment files 0-4 in 8_runner.py. 
This will get all the data ready for tuning. 
