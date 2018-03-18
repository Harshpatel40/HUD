import obd
from Tkinter import*
import time

root = Tk()

rpm1 = ''
rpm = Label(root, font=('times', 100, 'bold'), bg='black', fg='white')
rpm.pack(fill=BOTH, expand=1)

rpmConnection = obd.Async() # create an asynchronous connection
rpmConnection.watch(obd.commands.RPM) # keep track of RPM
rpmConnection.start() # start asynchronous connection for RPM

def printValues():
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
printValues()

root.mainloop()


