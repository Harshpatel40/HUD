import overpy
import sys
import simplejson as json

#pip install overpy
#python overpass_speed.py 37.7833 -122.4167 500
#python3 speed.py 40.503197 -74.385920 500

def maxspeed(coordinates, radius):
	lat, lon = coordinates
	api = overpy.Overpass()

# fetch all ways and nodes
	result = api.query("""
			way(around:""" + radius + """,""" + lat  + """,""" + lon  + """) ["maxspeed"];
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

results = maxspeed((sys.argv[1], sys.argv[2]), sys.argv[3])
print(results)
#print(json.dumps(results))