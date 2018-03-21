"""
Simple Program to help you get started with Google's APIs
"""
import urllib.request
import json
#Google MapsDdirections API endpoint
endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = 'AIzaSyAtnTpeJXirzSS7CRGaIntlXDcJ6V14EGM'
#Asks the user to input Where they are and where they want to go.
origin = input('Where are you?: ').replace(' ','+')
destination = input('Where do you want to go?: ').replace(' ','+')
#Building the URL for the request
nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
request = endpoint + nav_request
#Sends the request and reads the response.
response = urllib.request.urlopen(request).read()
#Loads response as JSON
directions = json.loads(response.decode('utf-8'))
print(directions)
#print(directions.keys())
routes = directions['routes']
#print(routes[0].keys())
legs = routes[0]['legs']
print("\n")
#iterate through the steps and print the html instructions (which are the directions) print distance for length of each step
stepslen= len(legs[0]['steps'])
for x in range(stepslen):
	print(legs[0]['steps'][x]['html_instructions'])
#total distance of trip
print(legs[0]['distance']['text'])
