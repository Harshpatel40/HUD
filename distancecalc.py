import math

lat1=40.527387
lng1=-74.436518

lat2=40.521819
lng2=-74.459581
def distance():
	global lat1
	global lng1
	global lat2
	global lng2
	radius = 3959  # mi
	dlat = math.radians(lat2-lat1)
	dlng = math.radians(lng2-lng1)
	a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
		* math.cos(math.radians(lat2)) * math.sin(dlng/2) * math.sin(dlng/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = radius * c
	return d

print(distance())