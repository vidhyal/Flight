#!/usr/bin/env python

import urllib
import json
import os
import sqlite3
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

conn = sqlite3.connect(':memory:')
flight_schedule_data = [
    ('ajaxair', '113', 'portland', '08:03', 'atlanta', '12:51', 'landed', ''),
    ('ajaxair', '114', 'atlanta', '14:05', 'portland', '16:44', 'boarding', ''),
    ('bakerair', '121', 'atlanta', '17:14', 'new york city', '19:20', 'departed', ''),
    ('bakerair', '122', 'new york city', '21:00', 'portland', '00:13', 'scheduled', ''),
    ('bakerair', '124', 'portland', '09:03', 'atlanta', '12:52', 'delayed', '09:55'),
    ('carsonair', '522', 'portland', '14:15', 'new york city', '16:58', 'scheduled', ''),
    ('carsonair', '679', 'new york city', '09:30', 'atlanta', '11:30', 'departed', ''),
    ('carsonair', '670', 'new york city', '09:30', 'portland', '12:05', 'departed', ''),
    ('carsonair', '671', 'atlanta', '13:20', 'new york city', '14:55', 'scheduled', ''),
    ('carsonair', '672', 'portland', '13:25', 'new york city', '20:36', 'scheduled', '')]

valid_data = { 
    'airlines': {'ajaxair', 'bakerair', 'carsonair'},
    'cities': {'portland', 'atlanta', 'new york city'},
    'status': {'landed', 'boarding', 'departed', 'scheduled', 'delayed'}
    }



    
c = conn.cursor()
c.execute('''create table flightSchedule(
  airline TEXT,
  flight_number INTEGER,
  departure_city TEXT,
  arrival_city TEXT,
  departure_time TEXT,
  arrival_time TEXT,
  status TEXT,
  delay_time TEXT,
  primary key(airline, flight_number)  
  );''')	
conn.commit()
c.executemany('insert into flightSchedule values (?,?,?,?,?,?,?,?)', flight_schedule_data)
  

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
    flightnumber = parameters.get("FlightNumber")
    print(result)
#    x = (getSchedule("flightnumber", flightnumber))
    c.execute('''select* from flightSchedule where flight_number=? ''', flightnumber)
    x= c.fetchall()
    if (x):
      x = x[0]
      speech = ('{} flight {} departs {} at {} and reaches {} at {}. It\'s status is{}'.format(*x) ) #str(x.airline) + " flight "+ str(x.flightnumber) +" departs "+ str(x.DepartureCity) + " at " + str(x.DepartureTime) + " and arrives at "+ str(x.ArrivalCity) + " at "+ str(x.ArrivalTime)
    else:
      speech = "cannot find that flight" + str(flightnumber)
    print ("you asked for flight "+str(flightnumber) )
    print("Response:")
    print (result)
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
    #makeTable()
    #printTable()
    #flightnumber =123
    #schedule = getSchedule("flightnumber", flightnumber)
    #for i in schedule:
    #  i.printSchedule()
    #x = (getSchedule("flightnumber", flightnumber))
    
    #if (x):
     # x = x[0]
      #speech = str(x.airline) + " flight "+ str(x.flightnumber) +" departs "+ str(x.DepartureCity) + " at " + str(x.DepartureTime) + " and arrives at "+ str(x.ArrivalCity) + " at "+ str(x.ArrivalTime)
    #else:
     # speech = "cannot find that flight"
    #print (speech)
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
