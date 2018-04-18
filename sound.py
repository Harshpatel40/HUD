import pygame
import threading
import time
x=1

def playsound():
	global x
	while 1:
		x=x+1
		time.sleep(1)
		#print(x)
		if x%2 == 0: 
			pygame.mixer.init()
			pygame.mixer.music.load("beep.mp3")
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy() == True:
			    continue

t=threading.Thread(target=playsound)
t.daemon=True
t.start()

while True:
	#x=x+1
	#time.sleep(1)
	print(x)    