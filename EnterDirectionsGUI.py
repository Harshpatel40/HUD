import urllib.request
import json

import tkinter
from tkinter import *

root = Tk()
root.title('Enter Directions')

root.geometry('{}x{}'.format(480,320))

Label(text='Starting Point?').pack(side=TOP,padx=10,pady=10)

entry = Entry(root, width=10)
entry.pack(side=TOP,padx=10,pady=10)

Label(text='Final Destination?').pack(side=TOP,padx=10,pady=10)

entry2 = Entry(root, width=10)
entry2.pack(side=TOP,padx=10,pady=10)


def onok():

	origin= entry.get()
	destination=entry2.get()

	#Google MapsDdirections API endpoint
	endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
	api_key = 'AIzaSyAtnTpeJXirzSS7CRGaIntlXDcJ6V14EGM'
	#Asks the user to input Where they are and where they want to go.

	origin=origin.replace(" ","+")
	destination=destination.replace(" ","+")




	# origin = input('Where are you?: ').replace(' ','+')
	# destination = input('Where do you want to go?: ').replace(' ','+')



	#Building the URL for the request

	print(origin)
	print(destination)

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

	print(stepslen)

	arraybuild(stepslen)


def arraybuild(numofsteps):


	arraylist=[15]
	arraylist2=[15]
	arraylist3=[15]
	arraylist4=[15]

	print(numofsteps)





	sys.exit()






Button(root, text='Get Directions', command=onok).pack(expand=True)

root.mainloop()

























