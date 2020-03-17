# Raspberry Pi GPIO Status and Control

from gpiozero import TimeOfDay, LED
#import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import datetime
from datetime import time

app = Flask(__name__)

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

# Define actuators GPIOs
ledRed = LED(15)
ledWhite = LED(3)
#ledRed = 15
#ledWhite = 3

# Initialize GPIO status variables
#ledRedSts = 0
#ledWhiteSts = 0

# Define led pins as output
#GPIO.setup(ledRed, GPIO.OUT)
#GPIO.setup(ledWhite, GPIO.OUT)

# Turn leds off
ledRed.off()
ledWhite.off()

#GPIO.output(ledRed, GPIO.LOW)
#GPIO.output(ledWhite, GPIO.LOW)

@app.route('/')

def index():
	# Read Status
	ledRedSts =  int(ledRed.is_lit)
	ledWhiteSts = int(ledWhite.is_lit)
	#ledRedSts = GPIO.input(ledRed)
	#ledWhiteSts = GPIO.input(ledWhite)
		
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	
	templateData = {
		'title' : 'RpiServer!',
		'time': timeString,
		'ledRed' : ledRedSts,
		'ledWhite' : ledWhiteSts
		}
	return render_template('index.html', **templateData)
	
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'ledRed':
		actuator = ledRed
	#if deviceName == 'ledWhite':
		#actuator = ledWhite
	
	if action == "on":
		#GPIO.output(actuator, GPIO.HIGH)
		actuator.on()
	if action == "off":
		#GPIO.output(actuator, GPIO.LOW)
		actuator.off()
		
	ledRedSts = int(ledRed.is_lit)
	ledWhiteSts = int(ledWhite.is_lit)
	
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	
	templateData = {
		'title' : 'RpiServer!',
		'time': timeString,
		'ledRed' : ledRedSts,
		'ledWhite' : ledWhiteSts
	}
	return render_template('index.html', **templateData)
	
@app.route("/handle_time", methods=['POST'])
def handle_time():
	startHour = int(request.form['sTimerH'])
	startMinute = int(request.form['sTimerM'])
	endHour = int(request.form['eTimerH'])
	endMinute = int(request.form['eTimerM'])
	tempo = TimeOfDay(time(startHour, startMinute),time(endHour, endMinute), utc=False)
	ledWhite.source = tempo
	
	ledRedSts = int(ledRed.is_lit)
	ledWhiteSts = int(ledWhite.is_lit)
	
	
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	
	templateData = {
		'title' : 'RpiServer!',
		'time': timeString,
		'ledRed' : ledRedSts,
		'ledWhite' : ledWhiteSts,
		'sHour' : startHour,
		'sMinute' : startMinute,
		'eHour' : endHour,
		'eMinute' : endMinute
	} 
	
	return render_template('index.html', **templateData)
		
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
	

