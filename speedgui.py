import obd
from Tkinter import*
import time

root = Tk()

speed1 = ''
speed = Label(root, font=('times', 100, 'bold'), bg='black', fg='white')
speed.pack(fill=BOTH, expand=1)

speedConnection = obd.Async() # create an asynchronous connection
speedConnection.watch(obd.commands.SPEED) # keep track of speed
speedConnection.start() # start asynchronous connection for speed

def printValues():
    global speed1
    # get the current speed from car
    speed2 = speedConnection.query(obd.commands.SPEED)
    # if speed string has changed, update it
    if speed2 != speed1:
        speed1 = speed2
        speed.config(text=speed2)
    # calls itself every 200 milliseconds
    # to update the speed display as needed
    speed.after(200, printValues)
printValues()

root.mainloop()


