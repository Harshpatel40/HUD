"""
Simple Program to help you get started with Google's APIs
"""
import urllib.request
import json
# global variables 
step_duration_list = []
step_startloc_lat_list = []
step_startloc_lng_list = []
step_endloc_lat_list = []
step_endloc_lng_list = []
step_html_list= []
step_maneuver_list = []


def directionsfunc(origin,destination):
	#Google MapsDdirections API endpoint
	endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
	api_key = 'AIzaSyAtnTpeJXirzSS7CRGaIntlXDcJ6V14EGM'
	origin = origin.replace(' ','+')
	destination = destination.replace(' ','+')
	#Building the URL for the request
	nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
	request = endpoint + nav_request
	#Sends the request and reads the response.
	response = urllib.request.urlopen(request).read()
	#Loads response as JSON
	directions = json.loads(response.decode('utf-8'))
	legs = directions['routes'][0]['legs']
	#iterate through the steps and print the html instructions (which are the directions) print distance for length of each step
	stepslen= len(legs[0]['steps'])
	print("number of steps: " + str(stepslen-1))
	# define lists as the global ones
	global step_duration_list
	global step_startloc_lat_list
	global step_startloc_lng_list
	global step_endloc_lat_list
	global step_endloc_lng_list
	global step_html_list
	global step_maneuver_list
	# clear the lists 
	del step_duration_list[:]
	del step_startloc_lat_list[:]
	del step_startloc_lng_list[:]
	del step_endloc_lat_list[:]
	del step_endloc_lng_list[:]
	del step_html_list[:]
	del step_maneuver_list[:]
	for x in range(stepslen):
		a=legs[0]['steps'][x]['duration']['text']
		step_duration_list.append(a)
		a=legs[0]['steps'][x]['start_location']['lat']
		step_startloc_lat_list.append(a)
		a=legs[0]['steps'][x]['start_location']['lng']
		step_startloc_lng_list.append(a)
		a=legs[0]['steps'][x]['end_location']['lat']
		step_endloc_lat_list.append(a)
		a=legs[0]['steps'][x]['end_location']['lng']
		step_endloc_lng_list.append(a)
		a=legs[0]['steps'][x]['html_instructions']
		step_html_list.append(a)

		if x==0:
			step_maneuver_list.append('none')
		else:
			a=legs[0]['steps'][x]['maneuver']
			step_maneuver_list.append(a)	
	return None 
