import pygame
import threading
import time
#lidar_distance in feet
lidar_distance=70
#car_speed is in mph
car_speed=50

def play_lidar_sound():
	global lidar_distance
	global car_speed
	while 1:
		time.sleep(1)
		#print("in thread")
		safe_distance=car_speed 
		if lidar_distance < safe_distance: 
			pygame.mixer.init()
			pygame.mixer.music.load("beep.mp3")
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy() == True:
			    continue

t=threading.Thread(target=play_lidar_sound)
t.daemon=True
t.start()

while True:
	#x=x+1
	time.sleep(1)
	#print(x)
	lidar_distance=lidar_distance-1
	print(lidar_distance)
	print("in main")    