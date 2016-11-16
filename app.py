#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
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


def makeTable():
	#table = []
	table.append(Schedule('AjaxAir', 113, 'Portland', 'Atlanta', '8:03 AM', '12:51 PM', 'Landed'))    
	table.append(Schedule('AjaxAir',114, 'Atlnata', 'Portland', '2:05 PM', '4:44 PM', 'Boarding'))
	table.append(Schedule('BakerAir', 121, 'Atlanta', 'New York', '5:14 PM', '7:20 PM', 'Departed'))
	table.append(Schedule('BakerAir', 122, 'New York', 'Portland', '9:00 PM', '12:13 AM', 'Scheduled'))
	table.append(Schedule('BakerAir', 124,	'Portland', 'Atlanta','9:03 AM', '12:52 PM' ,'Delayed to 9:55'))
	table.append(Schedule('CarsonAir', 522,	'Portland', 'New York', '2:15 PM', '4:58 PM', 'Scheduled'))
	table.append(Schedule('CarsonAir', 679,	'New York', 'Atlanta', '9:30 AM', '11:30 AM','Departed'))	
	table.append(Schedule('CarsonAir', 670,	'New York', 'Portland', '9:30 AM', '12:05 PM',	'Departed'))	
	table.append(Schedule('CarsonAir', 671,	'Atlanta', 'New York',	'1:20 PM','2:55 PM'	,'Scheduled'))
	table.append(Schedule('CarsonAir', 672,	'Portland','New York',	'1:25 PM', '8:36 PM','Scheduled'))	
	return table
	
def getSchedule(param, value):
  result =[]
  for x in table:
    if (getattr(x, param) == value):
      result.append(x)
  return result
  
def printTable():
	for x in table:
		x.printSchedule()


def makeWebhookResult(req):
    if req.get("result").get("action") != "getSchedule":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    flightnumber = parameters.get("flightnumber")

    x = (getSchedule("flightnumber", flightnumber))
    
    if (x):
      x = x[0]
      speech = str(x.airline) + " flight "+ str(x.flightnumber) +" departs "+ str(x.DepartureCity) + " at " + str(x.DepartureTime) + " and arrives at "+ str(x.ArrivalCity) + " at "+ str(x.ArrivalTime)
    else:
      speech = "cannot find that flight"
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "flightAgent"
    }

table =[]
if __name__ == '__main__':
    makeTable()
    #printTable()
    flightnumber =123
    #schedule = getSchedule("flightnumber", flightnumber)
    #for i in schedule:
    #  i.printSchedule()
    x = (getSchedule("flightnumber", flightnumber))
    
    if (x):
      x = x[0]
      speech = str(x.airline) + " flight "+ str(x.flightnumber) +" departs "+ str(x.DepartureCity) + " at " + str(x.DepartureTime) + " and arrives at "+ str(x.ArrivalCity) + " at "+ str(x.ArrivalTime)
    else:
      speech = "cannot find that flight"
    print (speech)
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
