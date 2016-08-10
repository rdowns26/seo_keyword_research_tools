
# Keyword Expansion Tool


INTRODUCTION
------------

The Keyword Expansion Tool uses the Google Adwords API Targeting Ideas Service to expand an input keyword into up to 500 related keywords with search volume.

  For a full description of the Targeting Ideas Service, visit the documentation page by Google:
  https://developers.google.com/adwords/api/docs/reference/v201605/TargetingIdeaService

This tool is made up of two pieces:
	Keyword_Expansion_Tool.py - This is the script you will run and edit. It takes inputs of keywords and ouputs a CSV with related keywords, average monthly search volume, language and location ID.

	Keyword_Planner_Ideas_Expansion.py - This script handles the API call to Google Adwords' Targeting Ideas Service. The Keyword Expansion Tool file imports this file as a module. Allow for separate configuration of API call.



REQUIREMENTS
------------

This module requires the following external modules:

	Time (documentation: https://docs.python.org/2/library/time.html)
	CSV (documentation: https://docs.python.org/2/library/csv.html)
	Googleads module (https://pypi.python.org/pypi/googleads)
	googleads.yaml Authentication File:
	  See Authentication instructions below

This module requires the following files in the same folder:

	Keyword_Expansion_Tool.py
	Keyword_Planner_Ideas_Expansion.py



AUTHENTICATION
-------------

You should have a googleads.yaml file that came with team-specific credentials. If you didn't there are instructions to follow here: 
	https://developers.google.com/adwords/api/docs/guides/first-api-call
	https://github.com/googleads/googleads-python-lib

Googleads.yaml should be in your home directory.



CONFIGURATION
-------------

There are 3 main parts to this script: the keyword(s) you want to expand, the language, and the location.

	Keyword(s):
		Option 1) uncomment lines 14-15 and create external file with one keyword per line called input_keywords.txt in same folder as this file
		
		Option 2) uncomment line 18 and write keywords directly into the list	
	
	Language ID:
		The ID can be found in the documentation: https://developers.google.com/adwords/api/docs/appendix/languagecodes
	
	Location ID: 
		The ID can be found in the documenation: https://developers.google.com/adwords/api/docs/appendix/geotargeting. Country codes found by searching country name in name filter



TROUBLESHOOTING
-------------

Hitting Rate Limits: Try running fewer keywords at a time (10 seems to work fine). The time.sleep(35) line should get past the 30 second rate limit, but sometimes there are still errors.


# Keyword Volume Tool

INTRODUCTION
------------

The Keyword Volume Tool uses the Google Adwords API Targeting Ideas Service to return the search volume and competition of a massive list of keywords.

	For a full description of the Targeting Ideas Service, visit the documentation page by Google: https://developers.google.com/adwords/api/docs/reference/v201605/TargetingIdeaService


REQUIREMENTS
------------

This module requires the following external modules:

	Time (documentation: https://docs.python.org/2/library/time.html)
	CSV (documentation: https://docs.python.org/2/library/csv.html)
	Suds (download: https://pypi.python.org/pypi/suds)
	Re (download: https://docs.python.org/2/library/re.html)
	Googleads module (https://pypi.python.org/pypi/googleads)
	googleads.yaml Authentication File: See Authentication instructions below


AUTHENTICATION
-------------

You should have a googleads.yaml file that came with team-specific credentials. If you didn't there are instructions to follow here: 
	https://developers.google.com/adwords/api/docs/guides/first-api-call
	https://github.com/googleads/googleads-python-lib

 Googleads.yaml should be in your home directory.



CONFIGURATION
-------------

There are 3 main parts to this script: the keyword(s) you want to get search volume for, the language, and the location.

	Keyword(s): Your input file should be called "input_file.txt" or you can change line 162
	
	Language ID: The ID can be found in the documentation: https://developers.google.com/adwords/api/docs/appendix/languagecodes
	
	Location ID: The ID can be found in the documenation: https://developers.google.com/adwords/api/docs/appendix/geotargeting
	Country codes found by searching country name in name filter


INSTRUCTIONS
-------------
Input: 
	input_file.txt 			- 	one keyword per line
Output: 
	result_input_file.txt 	- 	gives you keyword, monthly search volume, competition, keyword, location
	deleted_input_file.txt 	- 	documents duplicate keywords deleted from list, good to keep in mind
	duplicate_error.txt 	- 	logs any errors related to duplicate keywords, no action necessary


TROUBLESHOOTING
-------------

Hitting Rate Limits: Try running fewer keywords at a time (10 seems to work fine). The time.sleep(35) line should get past the 30 second rate limit, but sometimes there are still errors.
