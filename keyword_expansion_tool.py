# LOOK AT README.txt FIRST PLEASE!
import keyword_planner_ideas_expansion as EXP
import csv
import time

# CONFIGURATIONS
###########
# Options for importing keywords:
	# Option 1) uncomment lines 14-15 and create external file with one keyword per line
	# called input_keywords.txt in same folder as this file
	# Option 2) uncomment line 18 and write keywords directly into the list	

# OPTION 1:
#with open ("input_keywords.txt","r") as input_file:
	#keyword_list=[word.strip('\n') for word in input_file]

# OPTION 2:
keyword_list=['accounting']

# See README.txt about setting language and location.
langID=1000
locID=2356

############

count=1000
results={}
errors=[]

def write_to_file(current_results, current_word):

	with open("expanded_keywords.csv","a") as output_file:
		for key in current_results:
			word = key.encode('ascii','ignore')
			volume = current_results[key][0]
			competition = current_results[key][1]
			competition = "%.2f" % round(competition,2)
			#Write entry to file
			entry = current_word + ',' + word + ',' + str(volume) + ',' + str(competition) + ',' + str(langID) + ',' + str(locID) + '\n'
			output_file.write(entry)

with open("expanded_keywords.csv","a") as output_file:
	entry = "GROUP,KEYWORD,SEARCH_VOLUME,COMPETITION,LANG_CODE,LOC_CODE\n"
	output_file.write(entry)

for current_word in keyword_list:
	print "EXPANDING ... ",current_word
	try:
		current_results=EXP.ideas_expansion(current_word,langID,locID,count)
		write_to_file(current_results, current_word)
	except:
		errors.append(current_word)
	print "Please be patient and wait 40 seconds for rate limit compliance. Thank you :)"
	time.sleep(40)

print "THE FOLLOWING WORDS FAILED: ", errors