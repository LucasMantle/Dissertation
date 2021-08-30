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

In-order to run the code end-to-end, 8_runner.py can be run. You need to 
edit 8_runner.py to run the specific files you want.

There may be some issues when running some files and then running the tuning
files as they require different versions of pandas and numpy. 
To solve this issue, from parts 0-5, uninstall numpy and install it - this
should get the latest version. 
However, when running part 6, run 'pip install numpy==1.19.5'. 
