#!/usr/bin/env python
#
import urllib
import json
import os
import sqlite3
from flask import Flask
from flask import request
from flask import make_response
from datetime import datetime

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    print("Response:")
    print("Welcome to flight agent")
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

class Schedule():
	def __init__ (self, airline, flightnumber, DepartureCity, ArrivalCity, DepartureTime, ArrivalTime, Status):
		self.airline = airline
		self.flightnumber = flightnumber
		self.DepartureCity = DepartureCity
		self.ArrivalCity = ArrivalCity
		self.DepartureTime = DepartureTime
		self.ArrivalTime = ArrivalTime
		self.Status = Status
	def printSchedule(self):
		print (self.airline, self.flightnumber, self.DepartureCity, self.ArrivalCity, self.DepartureTime, self.ArrivalTime, self.Status)

cities = ['Atlanta', 'Portland', 'New York']
def makeTable():
	#table = []
	table.append(Schedule('AjaxAir', 113, 'Portland', 'Atlanta', '8:03AM', '12:51PM', 'Landed'))
	table.append(Schedule('AjaxAir',114, 'Atlanta', 'Portland', '2:05PM', '4:44PM', 'Boarding'))
	table.append(Schedule('BakerAir', 121, 'Atlanta', 'New York', '5:14PM', '7:20PM', 'Departed'))
	table.append(Schedule('BakerAir', 122, 'New York', 'Portland', '9:00PM', '12:13AM', 'Scheduled'))
	table.append(Schedule('BakerAir', 124,	'Portland', 'Atlanta','9:03AM', '12:52PM' ,'Delayed to 9:55'))
	table.append(Schedule('CarsonAir', 522,	'Portland', 'New York', '2:15PM', '4:58PM', 'Scheduled'))
	table.append(Schedule('CarsonAir', 679,	'New York', 'Atlanta', '9:30AM', '11:30AM','Departed'))
	table.append(Schedule('CarsonAir', 670,	'New York', 'Portland', '9:30AM', '12:05PM',	'Departed'))
	table.append(Schedule('CarsonAir', 671,	'Atlanta', 'New York',	'1:20PM','2:55PM'	,'Scheduled'))
	table.append(Schedule('CarsonAir', 672,	'Portland','New York',	'1:25PM', '8:36PM','Scheduled'))
	return table

def getSchedule(param, value):
  result =[]
  for x in table:
    if (getattr(x, param) == value):
      result.append(x)
  return result

def getSchedule1(paramVal):
    result =[]
    for x in table:
     val = True
     for i in paramVal:
       if (getattr(x, i[0]) != i[1]):
         val = False
         break
     if (val):
        result.append(x)
    return result

def getCityFrom(cityStr):
  for city in cities:
    if city in cityStr:
      return city
      
def getLongest(tab):
  Traveltime = {}
  longest = 0
  ind = 0
  strLong = ""
  for i in range (len(tab)):
    x,tt = getTravelTime(tab[i])
    if (tt>longest):
      longest = tt
      ind = i
      strLong = x
  return tab[i], strLong
    
def getShortest(tab):
  Traveltime = {}
  longest = 24*60*60
  ind = 0
  strLong = ""
  for i in range (len(tab)):
    x,tt = getTravelTime(tab[i])
    if (tt<longest):
      longest = tt
      ind = i
      strLong = x
  return tab[i], strLong    

def printTable():
	for x in table:
		x.printSchedule()

#there is a bug in this function
def getTravelTime (sch):
  initTime = datetime.strptime(sch.DepartureTime, '%I:%M%p')
  finTime = datetime.strptime(sch.ArrivalTime, '%I:%M%p')
  dur = finTime-initTime
  dur = dur.seconds//60
  duration = str(dur // 60 ) + " hrs  and "+str(dur % 60) + "mins"
  return duration, dur

def makeWebhookResult(req):
    foundIntent = False
    reqAction = req.get("result").get("action")

    if reqAction == "getStatus":
      foundIntent= True
      result = req.get("result")
      parameters = result.get("parameters")
      flightnumber = parameters.get("flightnumber")
      x = (getSchedule("flightnumber", int(flightnumber)))
      if (x):
        x = x[0]
        speech = "The status of "+ str(x.airline) + " flight "+ str(x.flightnumber) + " is " + str(x.Status)
      else:
        #can't understand why this gives an error.
        #I haven't found a bug here
        speech = "cannot find that flight " + str(flightnumber)
      #speech = "new hi"
      print("Response:")
      print(speech)

    if reqAction == "findStatus":
      foundIntent= True
      result = req.get("result")
      parameters = result.get("parameters")
      Status = paramters.get("Status")

      x = (getSchedule("Status",Status))

      if (x):
        speech = "Flights that have the status " + str(x[0].Status) + "are; "
        for n in x:
          speech += str(n.airline) + " flight " + str(n.flightnumber) + " "
      else:
        speech = "No flights have that status"
      print("Response:")
      print(speech)

    if reqAction == "getSchedule":
      foundIntent= True
      result = req.get("result")
      parameters = result.get("parameters")
      flightnumber = parameters.get("flightnumber")

      x = (getSchedule("flightnumber", int(flightnumber)))

      if (x):
        x = x[0]
        speech = str(x.airline) + " flight "+ str(x.flightnumber) +" departs "+ str(x.DepartureCity) + " at " + str(x.DepartureTime) + " and arrives at "+ str(x.ArrivalCity) + " at "+ str(x.ArrivalTime)
      else:
        speech = "cannot find that flight " + str(flightnumber)
      print("Response:")
      print(speech)

    if reqAction == "getDepartureTime":
      foundIntent= True
      result = req.get("result")
      parameters = result.get("parameters")
      flightnumber = parameters.get("flightnumber")
      x = (getSchedule("flightnumber", int(flightnumber)))

      if (x):
        x = x[0]
        speech = str(x.airline) + " flight "+ str(x.flightnumber) +" departs "+ str(x.DepartureCity) + " at " + str(x.DepartureTime)
      else:
        speech = "Cannot find that flight " + str(flightnumber)
      print("Response:")
      print(speech)

    if reqAction == "getArrivalTime":
      foundIntent= True
      result = req.get("result")
      parameters = result.get("parameters")
      flightnumber = parameters.get("flightnumber")
      x = (getSchedule("flightnumber", int(flightnumber)))

      if (x):
        x = x[0]
        speech = str(x.airline) + " flight "+ str(x.flightnumber) +" is expected to arrive at "+ str(x.ArrivalCity) + " at " + str(x.ArrivalTime)
      else:
        speech = "Cannot find that flight " + str(flightnumber)
      print("Response:")
      print(speech)

    if reqAction == "getTraveltime":
      foundIntent= True
      result = req.get("result")
      parameters = result.get("parameters")
      flightnumber = parameters.get("flightnumber")

      x = (getSchedule("flightnumber", int(flightnumber)))

      if (x):
        x = x[0]
        x1, dur = getTravelTime(x)
        speech = str(x.airline) + " flight "+ str(x.flightnumber) +" flies for  " + str(x1)
      else:
        speech = "cannot find that flight " + str(flightnumber)
      print("Response:")
      print(speech)

    if reqAction =="flightsBetween":
      foundIntent = True
      result = req.get("result")
      parameters = result.get("parameters")
      departcity = parameters.get("Departure_city")
      arrivecity = parameters.get("Arrival_City")
      
      departcity = getCityFrom(departcity)
      arrivecity = getCityFrom(arrivecity)
      x = (getSchedule1([["DepartureCity", departcity],["ArrivalCity", arrivecity]]))
      if (x):
        speech = "The flights available are:"
        for i in x:
          speech += str(i.airline) + " flight " + str(i.flightnumber)+ " departs " +str(i.DepartureCity)+" at " + str(i.DepartureTime) + " and reaches " +str(i.ArrivalCity) + " at " + str(i.ArrivalTime) +". "
      else:
        speech = "There are no direct flights in our database between the cities you asked"
      #speech = str(departcity)+ " " + str(arrivecity)
      print("Response:")
      print(speech)

    if reqAction =="getLongestBetween"  :
      foundIntent = True
      result = req.get("result")
      parameters = result.get("parameters")
      departcity = parameters.get("Departure_city")
      arrivecity = parameters.get("Arrival_City")
      
      departcity = getCityFrom(departcity)
      arrivecity = getCityFrom(arrivecity)
      x = (getSchedule1([["DepartureCity", departcity],["ArrivalCity", arrivecity]]))
      x1,tt = getLongest(x)
      if (x1):
        speech = "The longest flight from :" + str(x1.DepartureCity) +" to " +str(x1.ArrivalCity) +" is "+ str(x1.airline) +" flight "+ str(x1.flightnumber)+". It takes "+ str(tt)
      else:
        speech = "There are no direct flights in our database between the cities you asked"
      #speech = str(departcity)+ " " + str(arrivecity)
      print("Response:")
      print(speech)

      
    if reqAction =="getShortestBetween"  :
      foundIntent = True
      result = req.get("result")
      parameters = result.get("parameters")
      departcity = parameters.get("Departure_city")
      arrivecity = parameters.get("Arrival_City")
      
      departcity = getCityFrom(departcity)
      arrivecity = getCityFrom(arrivecity)
      x = (getSchedule1([["DepartureCity", departcity],["ArrivalCity", arrivecity]]))
      x1,tt = getShortest(x)
      if (x1):
        speech = "The shortest flight from :" + str(x1.DepartureCity) +" to " +str(x1.ArrivalCity) +" is "+ str(x1.airline) +" flight "+ str(x1.flightnumber)+". It takes "+ str(tt)
      else:
        speech = "There are no direct flights in our database between the cities you asked"
      #speech = str(departcity)+ " " + str(arrivecity)
      print("Response:")
      print(speech)  
    
    if (foundIntent):

      return {
          "speech": speech,
          "displayText": speech,
          #"data": {},
          # "contextOut": [],
          "source": "flightAgent"
      }

    else:
      return {
      }



table =[]
if __name__ == '__main__':
    makeTable()
    departcity = getCityFrom('fromAtlanta')
    arrivecity = getCityFrom('to Portland')
    departcity = getCityFrom(departcity)
    arrivecity = getCityFrom(arrivecity)
    x = (getSchedule1([["DepartureCity", departcity],["ArrivalCity", arrivecity]]))
    x1,tt = getLongest(x)
    if (x1):
      speech = "The longest flight from :" + str(x1.DepartureCity) +" to " +str(x1.ArrivalCity) +" is "+ str(x1.airline) +" flight "+ str(x1.flightnumber)+". It takes "+ str(tt)
    else:
      speech = "There are no direct flights in our database between the cities you asked"
    #speech = str(departcity)+ " " + str(arrivecity)
    print("Response:")
    print(speech)
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
