def ideas_expansion(keyword_list,langID,locID,count):

    from googleads import adwords
    adwords_client = adwords.AdWordsClient.LoadFromStorage()
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
        'requestType': 'IDEAS',
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
      try:
        for attribute in result['data']:
          if attribute['key']=="KEYWORD_TEXT":
            word=attribute['value']['value']
          if attribute['key']=="SEARCH_VOLUME":
            volume=attribute['value']['value']
          if attribute['key']=="COMPETITION":
            competition=attribute['value']['value']
        all_results[word]=[volume,competition]
      except AttributeError as e:
        e=e

    return all_results