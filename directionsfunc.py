"""
Simple Program to help you get started with Google's APIs
"""
import urllib.request
import json
import re
# global variables 
stepslen=0
step_distance_list = []
step_duration_list = []
step_startloc_lat_list = []
step_startloc_lng_list = []
step_endloc_lat_list = []
step_endloc_lng_list = []
step_html_list= []
step_maneuver_list = []

def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

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
	global stepslen
	stepslen= len(legs[0]['steps'])
	# define lists as the global ones
	global step_distance_list
	global step_duration_list
	global step_startloc_lat_list
	global step_startloc_lng_list
	global step_endloc_lat_list
	global step_endloc_lng_list
	global step_html_list
	global step_maneuver_list
	# clear the lists 
	del step_distance_list[:]
	del step_duration_list[:]
	del step_startloc_lat_list[:]
	del step_startloc_lng_list[:]
	del step_endloc_lat_list[:]
	del step_endloc_lng_list[:]
	del step_html_list[:]
	del step_maneuver_list[:]
	for x in range(stepslen):
		a=legs[0]['steps'][x]['distance']['text']
		step_distance_list.append(a)
		a=(legs[0]['steps'][x]['duration']['text']).split(' ')[0]
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
		a=cleanhtml(a)
		step_html_list.append(a)
		if ('maneuver' not in legs[0]['steps'][x]):		
			step_maneuver_list.append('none')
		else:
			a=legs[0]['steps'][x]['maneuver']
			step_maneuver_list.append(a)	
	return None 
def printdirections(x):
	#print the array you want
	print(str(x)+":"+ step_distance_list[x])
	print(str(x)+":"+ step_duration_list[x])
	print(str(x)+":"+ str(step_startloc_lat_list[x]))
	print(str(x)+":"+ str(step_startloc_lng_list[x]))
	print(str(x)+":"+ str(step_endloc_lat_list[x]))
	print(str(x)+":"+ str(step_endloc_lng_list[x]))
	print(str(x)+":"+ step_html_list[x])
	print(str(x)+":"+ step_maneuver_list[x])
	return None 

#main 
directionsfunc('rutgers','new brunswick')
for x in range(stepslen):
	printdirections(x)
directionsfunc('edison','metuchen')	
for x in range(stepslen):
	printdirections(x)
