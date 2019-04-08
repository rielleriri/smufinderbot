# references: 
# 	http://docs.python-requests.org/en/v0.6.1/api/#requests.models.Response
# 	https://core.telegram.org/bots/api
#   https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

import requests
import json
import datetime, time

###############################################################################################################################################
# global variables 
###############################################################################################################################################
#official bot token = '759354007:AAHq7todh18OVx0VVlMSAmplOtaBlQiE7wc'
#testing bot token = '827622553:AAH0ImyAKLVUlaXeMbGwrmifRYqlPJ1c5cE'

my_token = '738578681:AAHX5B7AwECaKBxNaHr90MsWYtydJzGo6J0' # put your secret Telegram token here 
url_base = 'https://api.telegram.org/bot{}/'.format(my_token)

smufinder_url_base = 'https://smufinderapi.herokuapp.com/'

#################################################################################################################################################
# The telegram API supports GET and POST HTTP methods.  e.g. getMe
# https://core.telegram.org/bots/api#available-methods 
# The HTTP URLs for each method looks like this: 
# https://api.telegram.org/bot{token}/{method_name}.
# The following defines the URLs for each method that we will use.
##################################################################################################################################################

# if you are not sure how each of these look like, you can print them (various methods available)
url_getUpdates = '{}getupdates'.format(url_base)
url_sendMsg = '{}sendMessage'.format(url_base)
url_sendPhoto = '{}sendPhoto'.format(url_base)

smufinder_get_itemtype = '{}itemtype/'.format(smufinder_url_base)
smufinder_get_location = '{}location/'.format(smufinder_url_base)
smufinder_get_facilities = '{}facility/'.format(smufinder_url_base)
smufinder_add_report = '{}reports'.format(smufinder_url_base)
smufinder_add_user = '{}users'.format(smufinder_url_base)

### START ########################################################################################################################################
#--GET/SET ALL OPTION ---------------------------------------------------------------------------------------------------------------------------------

#get itemtypes
item_types = []
r = requests.get(url = smufinder_get_itemtype)
for i in r.json():
	item_types.append(i['itemtype'])

#get location
locations = []
r = requests.get(url = smufinder_get_location)
for i2 in r.json():
	locations.append(i2['location_name'])
locations.append('Cannot Remember')

#get all facilities
facilities = []
r = requests.get(url = smufinder_get_facilities)
for i3 in r.json():
	facilities.append(i3['facilities_name'])

last_locations = ['The hive', 'Campus security', 'Same place item was found']
filters = [] #global variable
level = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14']


#--LOST OR FOUND -------------------------------------------------------------------------------------------------------------------------------

def lost_or_found(chat_id):
	# write code here 
	keyboard_button = [[{'text':"LOST"}], [{'text':"FOUND"}]] #array of arrays format for buttons, need 'text' key
	custom_keyboard = {'keyboard':keyboard_button, 'one_time_keyboard':True}
	reply_markup = json.JSONEncoder().encode(custom_keyboard) #encode in json format
	params = {'chat_id': chat_id , 'text':'Hello! Welcome to the official SMU Lost & Found bot. Use this bot to make a FOUND report or search for LOST items. You ONLY need to use the BUTTONS provided to key in details for each step. \n\nLet\'s begin! \n\nDid you lose or find something?', 'reply_markup': reply_markup} #https://core.telegram.org/bots/api#sendmessage
	requests.post(url_sendMsg, params)
	return 

#--FOUND -----------------------------------------------------------------------------------------------------------------------------------
def found(chat_id):
	keyboard_button = []
	one_row = []
	for i4 in range(0, len(item_types)):
		if i4 != (len(item_types)-1):
			if len(one_row)<1:
				one_row.append({'text': item_types[i4]})
			else:
				one_row.append({'text': item_types[i4]})
				keyboard_button.append(one_row)
				one_row = []
		else:
			if len(item_types)%2 == 0:
				keyboard_button.append(one_row)
			else:
				keyboard_button.append(one_row)
				one_row = []
				one_row.append({'text': item_types[i4]})
				keyboard_button.append(one_row)
				
	custom_keyboard = {'keyboard':keyboard_button, 'one_time_keyboard':True}
	reply_markup = json.JSONEncoder().encode(custom_keyboard) 
	params = {'chat_id': chat_id , 'text':'Please select item type from below.', 'reply_markup': reply_markup} 
	requests.post(url_sendMsg, params) #the append to list is in the listen and reply
	# photo(chat_id)
	return 

#--PHOTO ---------------------------------------------------------------------------------------------------------------------------------------
def photo(chat_id):
	params = {'chat_id': chat_id, 'text': 'Do you have a photo? Please upload photo or enter "na"'}
	requests.post(url_sendMsg, params)
	return


#--LOCATION------------------------------------------------------------------------------------------------------------------------------------
def location(chat_id):
	if filters[0] == "FOUND":
		locations.remove('Cannot Remember')
		keyboard_button = []
		one_row = []
		for i5 in range(0, len(locations)):
			if i5 != (len(locations)-1):
				if len(one_row)<1:
					one_row.append({'text': locations[i5]})
				else:
					one_row.append({'text': locations[i5]})
					keyboard_button.append(one_row)
					
					one_row = []
			else:
				if len(locations)%2 == 0:
					one_row.append({'text': locations[i5]})
					keyboard_button.append(one_row)
				else:
					keyboard_button.append(one_row)
					one_row = []
					one_row.append({'text': locations[i5]})
					keyboard_button.append(one_row)
		
		custom_keyboard = {'keyboard':keyboard_button, 'one_time_keyboard':True}
		reply_markup = json.JSONEncoder().encode(custom_keyboard) 
		params = {'chat_id': chat_id , 'text':'Please select a location.', 'reply_markup': reply_markup} 
		requests.post(url_sendMsg, params)
		return
	else:
		keyboard_button = []
		one_row = []
		for i5 in range(0, len(locations)):
			if i5 != (len(locations)-1):
				if len(one_row)<1:
					one_row.append({'text': locations[i5]})
				else:
					one_row.append({'text': locations[i5]})
					keyboard_button.append(one_row)
					
					one_row = []
			else:
				if len(locations)%2 == 0:
					one_row.append({'text': locations[i5]})
					keyboard_button.append(one_row)
				else:
					keyboard_button.append(one_row)
					one_row = []
					one_row.append({'text': locations[i5]})
					keyboard_button.append(one_row) 
		custom_keyboard = {'keyboard':keyboard_button, 'one_time_keyboard':True}
		reply_markup = json.JSONEncoder().encode(custom_keyboard) 
		params = {'chat_id': chat_id , 'text':'Please select a location.', 'reply_markup': reply_markup} 
		requests.post(url_sendMsg, params)
		return



#--LEVEL -------------------------------------------------------------------------------------------------------------------------------
def levels(chat_id):
	keyboard_button = [[{'text':"1"}, {'text':"2"},{'text':"3"}, {'text':"4"}, {'text':"5"}], 
						[{'text':"6"}, {'text':"7"},{'text':"8"}, {'text':"9"}, {'text':"10"}],
						[{'text':"11"}, {'text':"12"}, {'text':"13"}, {'text':"14"}],
					] 
	custom_keyboard = {'keyboard':keyboard_button, 'one_time_keyboard':True}
	reply_markup = json.JSONEncoder().encode(custom_keyboard) 
	params = {'chat_id': chat_id , 'text':'Please select the level.', 'reply_markup': reply_markup} 
	requests.post(url_sendMsg, params)
	return


#--FACILITY -------------------------------------------------------------------------------------------------------------------------------

def facility(chat_id):
	if filters[0] == "FOUND":
		location = filters[3]
		level = filters[4]
		loc_fac = []
		url = 'https://smufinderapi.herokuapp.com/facility/?location={}&level={}'.format(location,level)
		r = requests.get(url = url)
		for i4 in r.json():
			loc_fac.append(i4['facilities_name'])
		keyboard_button = []
		one_row = []
		for i5 in range(0, len(loc_fac)):
			if i5 != (len(loc_fac)-1):
				if len(one_row)<1:
					one_row.append({'text': loc_fac[i5]})
				else:
					one_row.append({'text': loc_fac[i5]})
					keyboard_button.append(one_row)
					
					one_row = []
			else:
				if len(loc_fac)%2 == 0:
					one_row.append({'text': loc_fac[i5]})
					keyboard_button.append(one_row)
				else:
					keyboard_button.append(one_row)
					one_row = []
					one_row.append({'text': loc_fac[i5]})
					keyboard_button.append(one_row)
		
		custom_keyboard = {'keyboard':keyboard_button, 'one_time_keyboard':True}
		reply_markup = json.JSONEncoder().encode(custom_keyboard) 
		params = {'chat_id': chat_id , 'text':'Please select a facility.', 'reply_markup': reply_markup} 
		requests.post(url_sendMsg, params)
		return
	else:
		location = filters[2]
		level = filters[3]
		loc_fac = []
		url = 'https://smufinderapi.herokuapp.com/facility/?location={}&level={}'.format(location,level)
		r = requests.get(url = url)
		for i4 in r.json():
			loc_fac.append(i4['facilities_name'])
		keyboard_button = []
		one_row = []
		for i5 in range(0, len(loc_fac)):
			if i5 != (len(loc_fac)-1):
				if len(one_row)<1:
					one_row.append({'text': loc_fac[i5]})
				else:
					one_row.append({'text': loc_fac[i5]})
					keyboard_button.append(one_row)
					
					one_row = []
			else:
				if len(loc_fac)%2 == 0:
					one_row.append({'text': loc_fac[i5]})
					keyboard_button.append(one_row)
				else:
					keyboard_button.append(one_row)
					one_row = []
					one_row.append({'text': loc_fac[i5]})
					keyboard_button.append(one_row)
		
		custom_keyboard = {'keyboard':keyboard_button, 'one_time_keyboard':True}
		reply_markup = json.JSONEncoder().encode(custom_keyboard) 
		params = {'chat_id': chat_id , 'text':'Please select a facility.', 'reply_markup': reply_markup} 
		requests.post(url_sendMsg, params)
		return


#--LAST LOCATION -------------------------------------------------------------------------------------------------------------------------------
def last_location(chat_id):
	keyboard_button = []
	one_row = []
	for i7 in range(0, len(last_locations)):
		if i7 != (len(last_locations)-1):
			if len(one_row)<1:
				one_row.append({'text': last_locations[i7]})
			else:
				one_row.append({'text': last_locations[i7]})
				keyboard_button.append(one_row)
				one_row = []
		else:
			if len(last_locations)%2 == 0:
				one_row.append({'text': last_locations[i7]})
				keyboard_button.append(one_row)
			else:
				keyboard_button.append(one_row)
				one_row = []
				one_row.append({'text': last_locations[i7]})
				keyboard_button.append(one_row) 
	custom_keyboard = {'keyboard':keyboard_button, 'one_time_keyboard':True}
	reply_markup = json.JSONEncoder().encode(custom_keyboard) 
	params = {'chat_id': chat_id , 'text':'Please select where item will be for pick-up.', 'reply_markup': reply_markup} 
	requests.post(url_sendMsg, params)
	return
	# return

#--LOST ---------------------------------------------------------------------------------------------------------------------------------------
def lost(chat_id):
	keyboard_button = []
	one_row = []
	for i4 in range(0, len(item_types)):
		if i4 != (len(item_types)-1):
			if len(one_row)<1:
				one_row.append({'text': item_types[i4]})
			else:
				one_row.append({'text': item_types[i4]})
				keyboard_button.append(one_row)
				one_row = []
		else:
			if len(item_types)%2 == 0:
				keyboard_button.append(one_row)
			else:
				keyboard_button.append(one_row)
				one_row = []
				one_row.append({'text': item_types[i4]})
				keyboard_button.append(one_row)
	custom_keyboard = {'keyboard':keyboard_button, 'one_time_keyboard':True}
	reply_markup = json.JSONEncoder().encode(custom_keyboard) 
	params = {'chat_id': chat_id , 'text':'Please select item type from below.', 'reply_markup': reply_markup} 
	requests.post(url_sendMsg, params)
	return 

#--ENDING FOR LOST ------------------------------------------------------------------------------------------------------------------------------
def match_results(chat_id):
	if len(filters) == 5:
		# ['LOST', 'Others', 'SIS', '3', 'SR-3-2']
		item_type = filters[1]
		found_location = filters[2]
		found_facilities = filters[4]
		url = 'https://smufinderapi.herokuapp.com/report/?item_type={}&found_location={}&found_facilities={}'.format(item_type, found_location, found_facilities)
		r = requests.get(url = url)
		rcopy = r.json()


		if len(rcopy)==0:
			params = {'chat_id': chat_id, 'text': 'Oh no there is no record that fits your filters! Please try again later.'}
			requests.post(url_sendMsg, params)
		elif len(rcopy) < 5:
			#send file to telegram and for the description will be in caption
			#variable caption
			for i in rcopy:
				file_id = i['photo']
				founder = i['founder']
				last_location = i['left_at_building']
				last_facilities = i['left_at_facilities']
				rid = str(i['rid'])

				if(file_id == 'No photos'):
					file_id = 'AgADBQADg6gxG0i1SVXYG-6sU34d7Yx33zIABAHNyq4-XUuWsWYDAAEC'

				url = 'https://smufinderapi.herokuapp.com/user/?chat_id={}'.format(founder)
				r2 = requests.get(url = url)
				rcopy2 = r2.json()

				foundername = rcopy2['username']
				
				caption = 'Report ID: '+ '/R' + rid + '\n' + 'Founder: ' + foundername + '\n' + 'Items at: ' + last_location + ', ' + last_facilities

				# ['LOST', 'Water Bottle', 'SIS', '2', 'SR-2-1']

				params2 = {'chat_id': chat_id, 'photo': file_id, 'caption': caption}
				requests.post(url_sendPhoto, params2)
			return
		else:
			url = 'https://smufinderapi.herokuapp.com/reportweb/?item_type={}&found_location={}&found_facilities={}'.format(item_type, found_location, found_facilities)
			new_url = url.replace(' ', '%20')
			msg = 'For a better viewing experience, view the results here: {}'.format(new_url)

			params = {'chat_id': chat_id, 'text': msg}
			requests.post(url_sendMsg, params)
		
		params3 = {'chat_id': chat_id, 'text': 'End of report. Hope you found your item ^ ^'}
		requests.post(url_sendMsg, params3)
		params4 = {'chat_id': chat_id, 'text': 'Please click on the report id. If you have collected the item.'}
		requests.post(url_sendMsg, params4)
	else:
		# ['LOST', 'Water Bottle', 'no location', 'no location']
		item_type = filters[1]
		url = 'https://smufinderapi.herokuapp.com/reportavailable/?itemtypes={}'.format(item_type)
		r = requests.get(url = url)
		rcopy = r.json()

		if len(rcopy)==0:
			params = {'chat_id': chat_id, 'text': 'Oh no there is no record that fits your filters! Please try again later.'}
			requests.post(url_sendMsg, params)
		elif len(rcopy) < 5:
			#send file to telegram and for the description will be in caption
			#variable caption
			for i in rcopy:
				file_id = i['photo']
				founder = i['founder']
				last_location = i['left_at_building']
				last_facilities = i['left_at_facilities']
				rid = str(i['rid'])

				if(file_id == 'No photos'):
					file_id = 'AgADBQADg6gxG0i1SVXYG-6sU34d7Yx33zIABAHNyq4-XUuWsWYDAAEC'

				url = 'https://smufinderapi.herokuapp.com/user/?chat_id={}'.format(founder)
				r2 = requests.get(url = url)
				rcopy2 = r2.json()

				foundername = rcopy2['username']
				
				caption = 'Report ID: '+ '/R' + rid + '\n' + 'Founder: ' + foundername + '\n' + 'Items at: ' + last_location + ', ' + last_facilities

				# ['LOST', 'Water Bottle', 'SIS', '2', 'SR-2-1']

				params2 = {'chat_id': chat_id, 'photo': file_id, 'caption': caption}
				requests.post(url_sendPhoto, params2)
		else:
			url = 'https://smufinderapi.herokuapp.com/reportweb2/?item_type={}'.format(item_type)
			new_url = url.replace(' ', '%20')
			msg = 'For a better viewing experience, view the results here: {}'.format(new_url)

			params = {'chat_id': chat_id, 'text': msg}
			requests.post(url_sendMsg, params)

		params3 = {'chat_id': chat_id, 'text': 'End of report. Hope you found your item ^ ^'}
		requests.post(url_sendMsg, params3)
		params4 = {'chat_id': chat_id, 'text': 'Please click on the report id. If you have collected the item.'}
		requests.post(url_sendMsg, params4)
	
	filters.clear()
	return

#-- GET THE USER INPUT AND COMPARE ------------------------------------------------------------------------------------------------------------
def listen_and_reply(chat_id, username, user_input, input_type):
	if input_type == 'photo':
		filters.append(user_input)
		location(chat_id)
	else:
		if user_input == "/start":
			#post the chat_id and username into database!!!!!!!!!!!!!!!!!!!!!!!
			params = {'chat_id': chat_id , 'username': username}
			requests.post(url = smufinder_add_user, json = params)
			lost_or_found(chat_id)

		elif user_input[0:2] == "/R":
			rid = int(user_input[2:])
			params4 = {'chat_id': chat_id, 'text': 'Thank you for using our bot ^ ^'}
			requests.post(url_sendMsg, params4)
			url = 'https://smufinderapi.herokuapp.com/reportretrieved/{}'.format(rid)
			requests.put(url = url)		

		elif user_input == "FOUND":
			filters.append(user_input)
			# lostfound = 'FOUND'
			found(chat_id)
		
		elif user_input in item_types:
			if filters[0] == "FOUND":
				filters.append(user_input) # e.g Wallet, found_report =['Wallet']
				photo(chat_id)
			elif filters[0] == "LOST":
				filters.append(user_input)
				location(chat_id)
		
		elif user_input.lower() == 'na':
			filters.append("No photos")
			location(chat_id)
		
		elif user_input == "LOST":
			filters.append(user_input)
			lost(chat_id)
			
		elif user_input in locations:
			if filters[0] == "FOUND":
				filters.append(user_input)
				levels(chat_id)
			else:
				if user_input == "Cannot Remember":
					filters.append("no location")
					filters.append("no location")
					match_results(chat_id)
				else:
					filters.append(user_input)
					levels(chat_id)
		
		elif user_input in level:
			filters.append(user_input)
			facility(chat_id)
		
		elif user_input in facilities:
			if filters[0] == "FOUND":
				filters.append(user_input)
				last_location(chat_id)
			else: #call function that generates matches found
				filters.append(user_input)
				match_results(chat_id)
				
		elif user_input in last_locations:
			if filters[0] == "FOUND":
				if user_input == 'Same place item was found':
					filters.append(filters[3])
					filters.append(filters[5])
					found_report = filters
					end(chat_id, found_report)
				elif user_input == 'The hive':
					filters.append('Li Ka Shing Library')
					filters.append('The Hive')
					found_report = filters
					end(chat_id, found_report)
				else:
					filters.append('Others')
					filters.append('Campus Security')
					found_report = filters
					end(chat_id, found_report)
			
			else: #last location not asked for lost so there is only one
				return None
		
		else:
			params = {'chat_id': chat_id, 'text': 'You\'ve exited your current request. Please click /start to begin a new one.'} 
			requests.post(url_sendMsg, params)
			filters.clear()
			return 



#--ENDING FOR FOUND ------------------------------------------------------------------------------------------------------------------------
def end(chat_id, found_report):
	params = {'chat_id': chat_id, 'text': 'Thank you for your kindness'}
	requests.post(url_sendMsg, params)
	
	item_desc = "null"
	photo = found_report[2]
	founder = chat_id
	item_type = found_report[1]
	found_location = found_report[3]
	found_facilities = found_report[5]
	last_location = found_report[6]
	last_facilities = found_report[7]

	params = {"item_desc": item_desc, "photo": photo, "founder": founder, "itemtype": item_type, "found_location": found_location, "found_facilities": found_facilities, "last_location": last_location, "last_facilities": last_facilities}
	requests.post(url = smufinder_add_report, json = params)

	# sample of found_report = ['FOUND', 'Handphone', 'No photos', 'SIS', 'SR-2-2', 'Others', 'Same place item was found']
	locations.append('Cannot Remember')
	filters.clear()
	return

#--GET LASTEST UPDATE --------------------------------------------------------------------------------------------------------------------------
def getting_last_update(updates):
	total_updates = len(updates["result"])
	last_updates = total_updates - 1
	chat_id = updates["result"][last_updates]["message"]["chat"]["id"]
	username = updates["result"][last_updates]["message"]["chat"]["username"]
	check_photo = updates["result"][last_updates]["message"]
	if "photo" in check_photo:
		user_input  = updates["result"][last_updates]["message"]["photo"][0]["file_id"]
		input_type = 'photo'
		return (user_input, chat_id, username, input_type)
	else:
		user_input  = updates["result"][last_updates]["message"]["text"]
		input_type = 'text'
		return (user_input, chat_id, username, input_type)


#--KEEP RUN THE FUNCTION----------------------------------------------------------------------------------------------------------------------------------

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url_base):
    content = get_url(url_base)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = url_base + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def main():
	last_update_id = None
	while True:
		updates = get_updates(last_update_id)
		if len(updates["result"]) > 0:
			last_update_id = get_last_update_id(updates) + 1
			user_input, chat_id, username, input_type = getting_last_update(updates)
			listen_and_reply(chat_id, username, user_input, input_type)
		time.sleep(0.5)

if __name__ == '__main__':
    main()

###############################################################################################################################################
# OLD CODES 
############################################################################################################################################
# I delete all the code
# url that i need
# https://github.com/michaelkrukov/heroku-python-script