#Entire Python Script for Keyword Research Using Keyword Planner API.

import csv
import time
import suds
import re
from googleads import adwords

####################
#API CALL FUNCTIONS
####################


def api_call_function(keyword_list, langID, locID, count):
		#print (adwords_client)
		#initializing appropriate service
		targeting_idea_service = adwords_client.GetService('TargetingIdeaService', version='v201605')
		
		offset = 0
		PAGE_SIZE = 100

		selector = {
				'searchParameters': [
						
						{
							'xsi_type': 'RelatedToQuerySearchParameter',
							'queries': keyword_list
					},
					{
							# Language setting (optional).
							# The ID can be found in the documentation:
							#  https://developers.google.com/adwords/api/docs/appendix/languagecodes
							'xsi_type': 'LanguageSearchParameter',
							'languages': [{'id': langID}]
					},
					{
							# Location setting (optional).
							# The ID can be found in the documenation:
							#  https://developers.google.com/adwords/api/docs/appendix/geotargeting
							# Country codes found by searching country name in name filter
							'xsi_type': 'LocationSearchParameter',
							'locations': [{'id': locID}]
					},
					{
							# Network search parameter (optional)
							'xsi_type': 'NetworkSearchParameter',
							'networkSetting': {
									'targetGoogleSearch': True,
									'targetSearchNetwork': False,
									'targetContentNetwork': False,
									'targetPartnerSearchNetwork': False

							}
					}

				],
				'ideaType': 'KEYWORD',
				'requestType': 'STATS',
				'requestedAttributeTypes': ['KEYWORD_TEXT','SEARCH_VOLUME','COMPETITION'],
				'paging': {
					'startIndex': str(offset),
					'numberResults': count
				}
		}

		page = targeting_idea_service.get(selector)

		#Create dictionary with keyword, search volume pair
		all_results={}
		for result in page['entries']:
			for attribute in result['data']:
				if attribute['key']=="KEYWORD_TEXT":
					word=attribute['value']['value']
				if attribute['key']=="SEARCH_VOLUME":
					volume=attribute['value']['value']
				if attribute['key']=="COMPETITION":
					competition=attribute['value']['value']
			all_results[word]=[volume, competition]

		return all_results


def api_call_error_handling(errors,current_call,i):
	
	def save_and_delete_keywords(keyword_file,error_lines):
		#delete bad keywords and log those deleted
		deleted_keyword_file = "deleted_" + keyword_file
		deleted_list = []
		with open(deleted_keyword_file,"a") as d_file:
			for bad_words in error_lines:
				deleted = current_call.pop(bad_words)
				deleted_list.append(deleted)
			for deleted in deleted_list:
				d_file.write(deleted + "\n")

	errors=str(errors)
	#log errors to file
	with open("duplicate_error.txt","a") as d_file:
		entry=  "ERROR - CALL # " + str(i+1) + "\n"
		d_file.write(entry)
		d_file.write(errors + "\n")
	#get line numbers from error reading
	error_lines = re.findall('\d\d*', errors)
	#clean "1"
	error_lines[:] = [int(x) for x in error_lines if len(x) != 1 ]
	error_lines.sort()
	error_lines.reverse()
	print (error_lines)
	save_and_delete_keywords(keyword_file,error_lines)
	return current_call


def get_estimate_search_volume(list_of_calls):
#Run estimate_search_volume for each set and add to result dictionary each time
	results = {}
	i = 0
	retry = False
	errors = "none"
	while i < num_calls:
		if retry == False:
			current_call = list_of_calls[i]
		try:
			call_results=api_call_function(current_call,langID,locID,800)
			print ("CALL #" ,i+1, "COMPLETED.")
			results.update(call_results)
			i += 1
			time.sleep(35)
			retry = False
		except suds.WebFault as e:
			errors = e
			print "ERROR LOGGED AS ERROR_LIST", e
			current_call = api_call_error_handling(errors,current_call,i)
			time.sleep(35)
			retry = True
			print ("LETS TRY THIS ONE AGAIN. CALL #", i+1)
	return results


def write_result_to_CSV (results,filename):
	#write result to a new CSV file
	filename.rstrip('.txt')
	filename = filename + ".csv"
	with open(filename,"w") as output_file:
		output_file.write("KEYWORD,MONTHLY_SEARCH_VOLUME,COMPETITION,LANG_ID,LOC_ID\n")
		for key in results:
			word = key
			volume = results[key][0]
			competition = results[key][1]
			#Write entry to file
			entry = word + ', ' + str(volume) + ', ' + str(competition) + ', ' + str(langID) + ', ' + str(locID) + '\n'
			output_file.write(entry)


####################
#SETTING UP SCRIPT
####################
if __name__ == '__main__':

	adwords_client = adwords.AdWordsClient.LoadFromStorage()

	###### READING FILE SET UP HERE ##########
	# Create external file with one keyword per line
	# called input_keywords.txt in same folder as this file
	keyword_file = "input_file.txt"
	langID = 1000
	locID = 2840

	#reading file
	with open(keyword_file,"rb") as keyword_list:
			#put keywords in local list
			before_estimate = [word.strip() for word in keyword_list]

	#set up queries for search volume
	list_of_calls = [before_estimate[i:i+200] for i in range(0, len(before_estimate), 200)]
	num_calls = len(list_of_calls)
	print ("Get ready for ", num_calls, "calls and approximately ", num_calls*50, "seconds.")

	####################
	#THE MAGIC HAPPENING
	####################

	results = get_estimate_search_volume(list_of_calls)
	write_result_to_CSV(results, "results_" + keyword_file)
