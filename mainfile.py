import urllib.request
import json
import time
#import obd
#import overpy
import sys
import simplejson as json
import tkinter
from tkinter import *
from PIL import ImageTk, Image


def raise_frame(frame):
    frame.tkraise()

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
	arraylist[0]="hello"
	arraylist2=[15]
	arraylist3=[15]
	arraylist4=[15]

	print(numofsteps)

	#sys.exit()



def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)


def printValuesSPEED():
    global rpm1
    # get the current RPM from car
    rpm2 = rpmConnection.query(obd.commands.RPM)
    # if rpm string has changed, update it
    if rpm2 != rpm1:
        rpm1 = rpm2
        rpm.config(text=str(rpm2).split('.')[0])
    # calls itself every 200 milliseconds
    # to update the rpm display as needed
    rpm.after(200, printValues)


def printValuesRPM():
    global rpm1
    # get the current RPM from car
    rpm2 = rpmConnection.query(obd.commands.RPM)
    # if rpm string has changed, update it
    if rpm2 != rpm1:
        rpm1 = rpm2
        rpm.config(text=str(rpm2).split('.')[0])
    # calls itself every 200 milliseconds
    # to update the rpm display as needed
    rpm.after(200, printValues)


def maxspeed(coordinates, radius):
	lat, lon = coordinates
	api = overpy.Overpass()

# fetch all ways and nodes
	result = api.query("""
			way(around:""" + str(radius) + """,""" + str(lat)  + """,""" + str(lon)  + """) ["maxspeed"];
				(._;>;);
					out body;
					    """)
	results_list = []
	returnspeed = 25
	for way in result.ways:
		road = {}
		road["name"] = way.tags.get("name", "n/a")
		road["speed_limit"] = way.tags.get("maxspeed", "n/a")
		# i deleted the coordinates of the speed limits  
		#nodes = []
		#for node in way.nodes:
		#    nodes.append((node.lat, node.lon))
		#road["nodes"] = nodes
		results_list.append(road)
		# return just one value
	if results_list:
		returnspeed = (results_list[0]['speed_limit']).split(' ')[0]

	return returnspeed
# returning only one speed limit
# do something where if there is no speed limit within 100 m of gps then return 0 to indicate no speed

def raise_frame_special(frame):
    frame.tkraise()
    directionsfunc()

def directionsfunc():
	# raise_frame(f5)
	origin= entry.get()
	destination=entry2.get()
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
		step_html_list.append(a)
		if ('maneuver' not in legs[0]['steps'][x]):		
			step_maneuver_list.append('none')
		else:
			a=legs[0]['steps'][x]['maneuver']
			step_maneuver_list.append(a)	
	
	for x in range(stepslen):
		printdirections(x)	

	

	raise_frame(f5)


	# ------------    PHOTO CODE     ------------

	# path="left.jpg"
	
	# if "right" in step_maneuver_list[0]:
	# 	path="right.jpg"

	# if "left" in step_maneuver_list[0]:
	# 	path="left.jpg"

	# if "straight" in step_maneuver_list[0]:
	# 	path="straight.jpg"

	# img=Image.open(path)
	# img=img.resize((80,80),Image.ANTIALIAS)
	# ph=ImageTk.PhotoImage(img)
	# line4=tkinter.Label(f5, image=ph)
	# line4.image=ph

#    ------------------------



	line1= Label(f5,bg='black',fg='white')
	line2= Label(f5,bg='black',fg='white')
	line3= Label(f5,bg='black',fg='white')
	# line4= Label(f5,bg='black',fg='white')
	line5= Label(f5,bg='black',fg='white')


	path="left.jpg"
	img=Image.open(path)
	img=img.resize((80,80),Image.ANTIALIAS)
	ph=ImageTk.PhotoImage(img)
	line4=tkinter.Label(f5, image=ph)
	line4.image=ph

	line1.pack()
	line2.pack()
	line5.pack()
	line4.pack()
	line3.pack()


	update_status(0,line1,line2, line3, line4, line5)
		

	return None 


def update_status(instructionholder,line1,line2, line3, line4, line5):

	line1["text"]=step_html_list[instructionholder]
	line2["text"]="Total Distance:" + step_distance_list[instructionholder]
	line5["text"]="Distance Remaining: 0.1 miles"
	line3["text"]="Current Speed Limit: 25"


	# if "right" in step_maneuver_list[instructionholder]:
	# 	line4["path"]="right.jpg"

	# if "left" in step_maneuver_list[instructionholder]:
	# 	line4["path"]="left.jpg"

	# if "straight" in step_maneuver_list[instructionholder]:
	# 	line4["path"]="straight.jpg"

	# line4.pack()
	# line3.pack()


	f5.update()
	time.sleep(5)

	print(instructionholder)
	instructionholder=instructionholder+1

	if(instructionholder>=stepslen):
		return None

	root.after(10000, update_status(instructionholder,line1,line2,line3,line4,line5))



	#-------
	# print(instructionholder)


	# if(instructionholder==0):
	# 	line1["text"]=step_html_list[0]
	# 	line2["text"]=step_distance_list[0]


	# if (instructionholder>0 & instructionholder < (stepslen-2)):
	# 	line1["text"]=step_html_list[instructionholder]
	# 	line2["text"]=step_distance_list[instructionholder]


	# if (instructionholder>(stepslen-2)):
	# 	return None

	# instructionholder=instructionholder+1


	# root.after(10000, update_status(instructionholder,line1,line2))

	#------

	#line1.pack()
	#line2.pack()
# .pack(side=TOP,pady=10)
# .pack(side=TOP,pady=10)

	# if (instructionholder>0):
	# 	instructionholder=instructionholder+1
	# 	line1["text"]=step_html_list[instructionholder]
	# 	line2["text"]=step_distance_list[instructionholder

	# line3= Label(f5,text=step_distance_list[instructionholder],bg='black',fg='white').pack(side=TOP,pady=10)
	# line4= Label(f5,text=step_distance_list[instructionholder],bg='black',fg='white').pack(side=TOP,pady=10)









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


#------------------------------------------------------------------------------------------------------------------------------------


root = Tk()
root.title('THUD')


root.geometry('{}x{}'.format(480,320))
root.configure(bg='black')









f1 = Frame(root,width=480, height=320)
f2 = Frame(root,width=480, height=320)
f3 = Frame(root,width=480, height=320)
f4 = Frame(root,width=480, height=320)
f5 = Frame(root,width=480, height=320)

f1.configure(bg='black')
f2.configure(bg='black')
f3.configure(bg='black')
f4.configure(bg='black')
f5.configure(bg='black')



for frame in (f1, f2, f3, f4, f5):
    frame.grid(row=0, column=0, sticky='news')





stepslen=0
step_distance_list = []
step_duration_list = []
step_startloc_lat_list = []
step_startloc_lng_list = []
step_endloc_lat_list = []
step_endloc_lng_list = []
step_html_list= []
step_maneuver_list = []


#-----------------------------------------------    FRAME   1      --------------------------------------------------------------------------------------

Label(f1,text='Starting Point?',bg='black',fg='white').pack(side=TOP,padx=150,pady=10)

entry = Entry(f1)
entry.pack(side=TOP,padx=150,pady=10)

Label(f1,text='Final Destination?',bg='black',fg='white').pack(side=TOP,padx=150,pady=10)

entry2 = Entry(f1)
entry2.pack(side=TOP,padx=150,pady=10)


# 	frame.tkraise()

button1=Button(f1, highlightbackground='black', text='Get Directions', command=lambda:raise_frame_special(f5)).pack(expand=True,pady=5)


#button2=Button(f1, highlightbackground='black', text='Begin', command=lambda:raise_frame(f5)).pack(pady=5)


button3=Button(f1, highlightbackground='black', text='Go to frame 2', command=lambda:raise_frame(f2)).pack(pady=30)




#--------------------------------------------------     FRAME 2      --------------------------------------------------------------------------------


Label(f2,text='Time',bg='black',fg='white').pack(side=TOP,pady=10)

time1 = ''
clock = Label(f2, font=('times', 100, 'bold'), bg='black', fg='white')
clock.pack(fill=BOTH, expand=1)

tick()

button4=Button(f2, highlightbackground='black', text='Go to frame 3', command=lambda:raise_frame(f3)).pack(pady=50)




#-----------------------------------------------------     FRAME 3      --------------------------------------------------------------------------------


Label(f3,text='Speed / RPM',bg='black',fg='white').pack(side=TOP,pady=10)


button5=Button(f3, highlightbackground='black', text='Go to frame 4', command=lambda:raise_frame(f4)).pack(pady=50)


#  -------------        SPEED       --------------
# speed1 = ''
# speed = Label(f3, font=('times', 100, 'bold'), bg='black', fg='white')
# speed.pack(fill=BOTH, expand=1)

#speedConnection = obd.Async() # create an asynchronous connection
#speedConnection.watch(obd.commands.SPEED) # keep track of speed
#speedConnection.start() # start asynchronous connection for speed

#printValuesSPEED()

#  -------------        RPM       ----------------
# rpm1 = ''
# rpm = Label(f3, font=('times', 100, 'bold'), bg='black', fg='white')
# rpm.pack(fill=BOTH, expand=1)

#rpmConnection = obd.Async() # create an asynchronous connection
#rpmConnection.watch(obd.commands.RPM) # keep track of RPM
#rpmConnection.start() # start asynchronous connection for RPM

#printValuesRPM()




#----------------------------------------------------     FRAME 4        ---------------------------------------------------------------------------------

Label(f4,text='OBD Diagnostics',bg='black',fg='white').pack(side=TOP,pady=10)
Label(f4,text='No alerts at this moment!',bg='black',fg='white').pack(side=TOP,pady=20)


button6=Button(f4, highlightbackground='black', text='Go to frame 1', command=lambda:raise_frame(f1)).pack(pady=50)



#----------------------------------------------------     FRAME 5        ---------------------------------------------------------------------------------


Label(f5,text='DIRECTIONS',bg='black',fg='white').pack(side=TOP,pady=10)
# button100=Button(f5, highlightbackground='black', text='start', command=lambda:directionsfunc)


# Label(f5,text='Distance',bg='black',fg='white').pack(side=TOP,pady=10)
# Label(f5,text='Remaining Distance',bg='black',fg='white').pack(side=TOP,pady=10)

# # PICTURE

# Label(f5,text='Current Speed Limit',bg='black',fg='white').pack(side=TOP,pady=10)











#-------------------------------------------------------------------------------------------------------------------------------------------



raise_frame(f1)

root.mainloop()

























