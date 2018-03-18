import obd
from Tkinter import*
import time

root = Tk()

topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side = BOTTOM)

speed1 = ''
speed = Label(topFrame, bg='black', fg='white')
speed.pack(fill=BOTH, expand=1)

rpm1 = ''
rpm = Label(bottomFrame, bg='black', fg='white')
rpm.pack(fill=BOTH, expand=1)

speedConnection = obd.Async() # create an asynchronous connection
speedConnection.watch(obd.commands.SPEED) # keep track of speed
speedConnection.start() # start asynchronous connection for speed

rpmConnection = obd.Async() # create an asynchronous connection
rpmConnection.watch(obd.commands.RPM) # keep track of RPM
rpmConnection.start() # start asynchronous connection for RPM

def printValues():
    global speed1
    global rpm1
    # get the current speed from car
    speed2 = speedConnection.query(obd.commands.SPEED)
    # get the current RPM from car
    rpm2 = rpmConnection.query(obd.commands.RPM)
    # if rpm string has changed, update it
    # if speed string has changed, update it
    if speed2 != speed1:
        speed1 = speed2
        speed.config(text=speed2)
    if rpm2 != rpm1:
        rpm1 = rpm2
        rpm.config(text=str(rpm2).split('.')[0])
    # calls itself every 200 milliseconds
    # to update the rpm display as needed
    rpm.after(200, printValues)
printValues()

root.mainloop()
