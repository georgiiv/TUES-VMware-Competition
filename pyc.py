import urllib2
import requests
import networkx as nx
import matplotlib.pyplot as pltimport
import time
import string
import sys

g = nx.DiGraph()
location = sys.argv[2]
location = int(location)

HOST_URL="http://130.204.92.143:8080"
OBJECTS_API = "/api/sector/%d/objects"
ROOTS_API = "/api/sector/%d/roots"
POST_URL = HOST_URL + "/api/sector/" + str(location)+ "/company/pastetmanja/trajectory"

def get_objects(sector):
	url = HOST_URL + OBJECTS_API % sector
	print
	print url

	res=urllib2.urlopen(url)
	edges = []
	for line in res.readlines(): 
		edges.append( [int(s) for s in line.strip().split(' ')] )
	return edges
	

def get_roots(sector):
	url = HOST_URL + ROOTS_API % sector
	print
	print url

	res=urllib2.urlopen(url)
	nodes = []
	for line in res.readlines():
		nodes.append(int(line.strip()))
	return nodes


edges = get_objects(location)


mama = []

for x in edges:
	a = x[0]
	b = x[1]
	mama.append(a)
	mama.append(b)

size = max(mama)

g.add_node(size)

roots = get_roots(location)


for z in edges:
	y=z[0]
	x=z[1]
	g.add_edge(y,x)
#print (g.number_of_nodes())
#print (g.number_of_edges())
list1 = list()
list2 = list()
for x in roots:
	list1.append(list(nx.dfs_edges(g,x)))



for x in list1:
	for y in x:
		list2.append(y[0])
		list2.append(y[1])
		
 
set1 = set()
for x in list2:
	set1.add(x)
	
for x in set1:
	g.remove_node(x)
	
#print(g.number_of_nodes())	
#print(g.number_of_edges())


#============================================================================================


cyka1 = list()
cyka1.append(list(nx.dfs_edges(g)))

last = -1
i = 0

stan = ""
startcon = 0

for a in cyka1[0]:
	if (a[0] != last):
		if (startcon == 1):
			payload = {'trajectory': stan}
			r = requests.post(POST_URL, data = payload)
			#print(r.status_code)
		#print(stan)
		startcon = 1
		stan = str(a[0])+ " " + str(a[1])
		last = a[1]
	if (last == a[0]):
		last = a[1]
		stan = stan+ " " + str(a[1])
