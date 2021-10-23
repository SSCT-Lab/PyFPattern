# PyFPattern
Mining Python Fix Patterns via Analyzing Fine-Grained Source Code Changes

# Structure of the Directories: 

※Data Set: 
Data Set folder contains the experimental data, divided into five sub-sub-folders, according to the granularity of differences in the bug-fixing files. 

Bug-fixing-1 and bug-fixing-2 contain single hunk bugs, and bug fix only add/del code statements. 

Bug-fixing-3 and bug-fixing-4 mainly contain code changes in multiple locations but in a single function. 

Bug-fixing-5 mainly contains code changes in multiple locations but in one file. 

※Test Set:
Open Source Projects: four open source project datasets (tensorlayer,powerline,mopidy,flask)

QuixBugs (Python): https://jkoppel.github.io/QuixBugs/ 
