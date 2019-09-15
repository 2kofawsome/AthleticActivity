#! python3.6

#https://www.strava.com/oauth/authorize?client_id=38950&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read
    
"""{
    "token_type": "Bearer",
    "access_token": "ff95a3c12476ca93a68825a38688dc72fb164e62",
    "athlete": {
        "id": 25997915,
        "username": "awsome2",
        "resource_state": 2,
        "firstname": "Sam",
        "lastname": "Gunter",
        "city": "Peterborough",
        "state": "ON",
        "country": null,
        "sex": "M",
        "premium": false,
        "summit": false,
        "created_at": "2017-10-31T20:53:13Z",
        "updated_at": "2019-06-22T02:28:48Z",
        "badge_type_id": 0,
        "profile_medium": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/25997915/12282949/1/medium.jpg",
        "profile": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/25997915/12282949/1/large.jpg",
        "friend": null,
        "follower": null
    }
}"""


from stravalib.client import Client

client = Client(access_token="ff95a3c12476ca93a68825a38688dc72fb164e62 ")
activities = client.get_activities(limit=10)

run = client.get_activity(list(activities)[0].id)

# Activities can have many streams, you can request n desired stream types
types = ['time', 'latlng', 'altitude', 'distance']

streams = client.get_activity_streams(list(activities)[0].id, types=types, resolution='high')

#  Result is a dictionary object.  The dict's key are the stream type.

heights = streams['altitude'].data
cords = streams['latlng'].data
times = streams['time'].data
distances = streams['distance'].data

csvData = [['x', 'y', 'z']]

import csv
from datetime import datetime


pacePoints = 0
paceSum = 0
paces = [[]]


x = 0
lastD = 0
lastT = 0
for n in range(len(times)): #x, y, z, speed
    csvData.append([cords[n][0], cords[n][1], heights[n]])

    
    DDif = distances[n] - lastD
    lastD = distances[n]
    TDif = times[n] - lastT
    lastT = times[n]

    if DDif == 0:
        pace = 0
    else:
        pace = 26.82233333/DDif*TDif

    pacePoints += 1
    paceSum += pace
    if distances[n] / 1000 > len(paces):
        paces.append([])
    paces[-1].append(pace)

average = paceSum / pacePoints

paceData = []
for n in range(len(paces)):
    x = n
    below = 0
    above = 0
    for m in paces[n]:
        if m <= average:
            below += 1
        else:
            above += 1
    paceData.append([x, above, below])

with open('route.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)
csvFile.close()

with open('bar.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(paceData)
csvFile.close()

xMax = csvData[1][0]
xMin = csvData[1][0]
yMax = csvData[1][1]
yMin = csvData[1][1]
for n in csvData[1:]:
    if n[0] > xMax:
        xMax = n[0]
    if n[0] < xMin:
        xMin = n[0]
    if n[1] > yMax:
        yMax = n[1]
    if n[1] < yMin:
        yMin = n[1]

xMin = float(xMin)
yMin = float(yMin)
xMax = float(xMax)
yMax = float(yMax)

if xMax - xMin > yMax - yMin:
    add = ((xMax - xMin) - (yMax - yMin))/2
    yMax += add
    yMin -= add
elif yMax - yMin > xMax - xMin:
    add = ((yMax - yMin)-(xMax - xMin))/2
    xMax += add
    xMin -= add

###################################################33

import json
import urllib.request
import math

def elevation(lat1, lng1, lat2, lng2, smpls):
    global elevation_matrix
    apikey = "AIzaSyDjTjrZdOAQ2hZ4fTo-jyqO5wXs1FqptBY" 
    url = "https://maps.googleapis.com/maps/api/elevation/json" 
    request = urllib.request.urlopen(url+"?path="+str(lat1)+","+str(lng1)+"|"+str(lat1)+","+str(lng2)+"&samples="+str(smpls)+"&key="+apikey) 
    results = json.load(request).get('results') 
    for i in range(0, smpls): 
        if 0 < len(results):
            elevation_matrix.append([lat1, lng1+i*((lng2-lng1)/smpls), results[i].get('elevation')])
            

def elevation_path(lat1, lng1, lat2, lng2, smpls): 
    global elevation_matrix
    int_dist = abs(lng2 - lng1) / smpls
    smpls_2 = math.ceil(abs(lat2 - lat1) / int_dist)
    elevation_matrix = []
    print(smpls)
    print(smpls_2)
    for i in range(smpls_2): 
        elevation(lat1+i*int_dist, lng1, lat2+i*int_dist, lng2, smpls)


elevation_path(xMin, yMin, xMax, yMax, 20)
###################################################33

with open('terrain.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(elevation_matrix)
csvFile.close()

with open('altitude.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(alt_matrix)
csvFile.close()



