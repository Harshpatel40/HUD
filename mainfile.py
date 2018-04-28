import urllib.request
import json
import time
import re
import obd
import overpy
import sys
import simplejson as json
import tkinter
from tkinter import *
from PIL import ImageTk, Image
import serial
import time
import subprocess
import os
import pygame
import threading

#----------------------------------------  FUNCTIONS  BEGIN    ------------------------------------------------

def raise_frame(frame):
    frame.tkraise()

def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

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
    global speed1
    # get the current RPM from car
    speed2 = speedConnection.query(obd.commands.SPEED)
    # if rpm string has changed, update it
    if speed2 != speed1:
        speed1 = speed2
        speed.config(text=speed2)
    # calls itself every 200 milliseconds
    # to update the rpm display as needed
    speed.after(200, printValues)


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
		a=cleanhtml(a)
		step_html_list.append(a)
		if ('maneuver' not in legs[0]['steps'][x]):		
			step_maneuver_list.append('none')
		else:
			a=legs[0]['steps'][x]['maneuver']
			step_maneuver_list.append(a)	
	
	for x in range(stepslen):
		printdirections(x)	

	raise_frame(f5)

	line1= Label(f5,bg='black',fg='white')
	line2= Label(f5,bg='black',fg='white')
	line3= Label(f5,bg='black',fg='white')
	# line4= Label(f5,bg='black',fg='white')
	line5= Label(f5,bg='black',fg='white')

	path="none.jpg"
	img=Image.open(path)
	# img=img.resize((80,80),Image.ANTIALIAS)
	ph=ImageTk.PhotoImage(img)
	line4=tkinter.Label(f5, image=ph, borderwidth=0, highlightthickness=0)
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
	line3["text"]="Current Speed Limit: 25 MPH" # + str(maxspeed((40.516972, -74.435804),50))

	img=ImageTk.PhotoImage(Image.open(step_maneuver_list[instructionholder]+".jpg"))
	line4.configure(image=img)
	line4.image=img

	f5.update()
	time.sleep(5)

	print(instructionholder)
	instructionholder=instructionholder+1

	if(instructionholder>=stepslen):
		return None

	root.after(10000, update_status(instructionholder,line1,line2,line3,line4,line5))

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


def leftKey(event):
	
	global currentframe
		
	if (currentframe==1):
		currentframe=7
		raise_frame(f7)

	elif (currentframe==2):
		currentframe=1
		raise_frame(f1)

	elif (currentframe==3):
		currentframe=2
		raise_frame(f2)

	elif (currentframe==4):
		currentframe=3
		raise_frame(f3)
	elif (currentframe==6):
		currentframe=4
		raise_frame(f4)
	elif (currentframe==7):
		currentframe=6
		raise_frame(f6)
	else:
		currentframe=1
		raise_frame(f1)

	print("Left Key pressed")


def rightKey(event):

	global currentframe

	if (currentframe==1):
		currentframe=2
		raise_frame(f2)

	elif (currentframe==2):
		currentframe=3
		raise_frame(f3)

	elif (currentframe==3):
		currentframe=4
		raise_frame(f4)

	elif (currentframe==4):
		currentframe=6
		raise_frame(f6)
	elif (currentframe==6):
		currentframe=7
		raise_frame(f7)
	elif (currentframe==7):
		currentframe=1
		raise_frame(f1)
	else:
		currentframe=1
		raise_frame(f1)

	print("Right key pressed")


# -------------------   LIDAR CODE --------------------------- 


root=Tk()


lidar_distance=100.0
lidar_distancelabel=IntVar()
lidar_distancelabel.set(0)

current_speed=0

def run_lidar():
    ser = serial.Serial('/dev/ttyUSB1',115200,timeout = 1)
    ser.write(bytes(b'B'))
    ser.write(bytes(b'W'))
    ser.write(bytes(2))
    ser.write(bytes(0))
    ser.write(bytes(0))
    ser.write(bytes(0))
    ser.write(bytes(1))
    ser.write(bytes(6))

    global lidar_distance
    global current_speed

    while(True):
        time.sleep(1)
        while(ser.in_waiting >= 9):
            if((b'Y' == ser.read()) and ( b'Y' == ser.read())):
                Dist_L = ser.read()
                Dist_H = ser.read()
                Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
                for i in range (0,5):
                    ser.read()
            lidar_distance=Dist_Total/30.48
            lidar_distancelabel.set(lidar_distance)
            if lidar_distance < 5 :
                pygame.mixer.init()
                pygame.mixer.music.load("beep.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    continue
        print(lidar_distance)

t=threading.Thread(target=run_lidar)
t.daemon=True
t.start()

# -------------------   GPS  CODE --------------------------- 

def getLat():

	python3_command = "python getLat.py"
	process=subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
	output=output.decode('utf8')
	return(output)

def getLon():

	python3_command = "python getLon.py"
	process=subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
	output=output.decode('utf8')
	return(output)

current_speed_label=IntVar()
current_speed_label.set(0)


def getSpeed():

	python3_command = "python getSpeed.py"
	process=subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
	output, error= process.communicate()
	output=output.decode('utf8')
	global current_speed
	current_speed=output
	current_speed_label.set(output)
	return(output)


speedthread=threading.Thread(target=getSpeed)
speedthread.daemon=True
speedthread.start()


#   --------------------   MUSIC PLAYER  CODE    ------------------








#----------------------------------------  FUNCTIONS  END    ------------------------------------------------


root.title('THUD')


root.geometry('{}x{}'.format(800,480))
root.configure(bg='black')


f1 = Frame(root,width=800, height=480)
f2 = Frame(root,width=800, height=480)
f3 = Frame(root,width=800, height=480)
f4 = Frame(root,width=800, height=480)
f5 = Frame(root,width=800, height=480)
f6 = Frame(root,width=800, height=480)
f7 = Frame(root,width=800, height=480)


currentframe = 1

f1.configure(bg='black')
f2.configure(bg='black')
f3.configure(bg='black')
f4.configure(bg='black')
f5.configure(bg='black')
f6.configure(bg='black')
f7.configure(bg='black')


for frame in (f1, f2, f3, f4, f5, f6, f7):
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


button1=Button(f1, highlightbackground='black', text='Get Directions', command=lambda:raise_frame_special(f5)).pack(expand=True,pady=5)



#--------------------------------------------------     FRAME 2      --------------------------------------------------------------------------------


Label(f2,text='Time',bg='black',fg='white').pack(side=TOP,pady=10)

time1 = ''
clock = Label(f2, font=('times', 100, 'bold'), bg='black', fg='white')
clock.pack(fill=BOTH, expand=1)

tick()





#-----------------------------------------------------     FRAME 3      --------------------------------------------------------------------------------



Label(f3,text='Speed', bg='black',fg='white').pack(side=TOP,pady=10)
Label(f3,textvariable=current_speed_label, bg='black',fg='white').pack(side=TOP,pady=10)

# button5=Button(f3, highlightbackground='black', text='Go to frame 4', command=lambda:raise_frame(f4)).pack(pady=50)



#----------------------------------------------------     FRAME 4        ---------------------------------------------------------------------------------

Label(f4,text='OBD Diagnostics',bg='black',fg='white').pack(side=TOP,pady=10)
Label(f4,text='No alerts at this moment!',bg='black',fg='white').pack(side=TOP,pady=20)




#----------------------------------------------------     FRAME 5        ---------------------------------------------------------------------------------


Label(f5,text='DIRECTIONS',bg='black',fg='white').pack(side=TOP,pady=10)






#    MUSIC PLAYER CODE
Label(f6,text='MUSIC PLAYER',bg='black',fg='white').pack(side=TOP,pady=10)

listofsongs = []
v = StringVar()
songlabel = Label(f6,textvariable=v,width=35)
index = 0




def directorychooser():
    directory="/home/pi/Desktop"
    os.chdir(directory)

    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            listofsongs.append(files)

    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[0])
    pygame.mixer.music.play()

directorychooser()

def updatelabel():
    global index
    global songname
    v.set(listofsongs[index])

def nextsong(event):
    global index
    if index<len(listofsongs)-1:
        index += 1
    else:
        index=0
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def prevsong(event):
    global index
    if index>0:
        index -= 1
    else:
        index=len(listofsongs)-1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def stopsong(event):
    pygame.mixer.music.stop()
    v.set("")

def playsong(event):
    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

listbox = Listbox(f6)
listbox.pack()

listofsongs.reverse()

for items in listofsongs:
    listbox.insert(0,items)

listofsongs.reverse()

nextbutton = Button(f6,text = 'Next Song')
nextbutton.pack()

previousbutton = Button(f6,text = 'Previous Song')
previousbutton.pack()

stopbutton = Button(f6,text='Stop Music')
stopbutton.pack()

playbutton = Button(f6,text='Play Music')
playbutton.pack()



#    LIDAR  CODE

Label(f7,text='LIDAR TEST',bg='black',fg='white').pack(side=TOP,pady=10)




#-------------------------------------------------------------------------------------------------------------------------------------------


raise_frame(f1)


root.bind('<Left>',leftKey)
root.bind('<Right>',rightKey)

nextbutton.bind("<Button-1>",nextsong)
previousbutton.bind("<Button-1>",prevsong)
stopbutton.bind("<Button-1>",stopsong)
playbutton.bind("<Button-1>",playsong)
songlabel.pack()

root.mainloop()


