# Needed Libraries
import serial
import time
import os
import requests
import serial.tools.list_ports
import datetime

# Color-Codes
warmColor = "FFFF00"
clearColor = "FFCC88"
rainyColor = "00FFFF"
coldColor = "40E0D0"
windyColor = "88CCFF"

# Animations
ani_Warm = "303"
ani_Clear = "303"
ani_Rainy = "105"
ani_Cold = "151"
ani_Windy = "212"
ani_Cloudy = "242"

# Brightness Value of the LEDs
br_Warm = "100"
br_Clear = "32"
br_Rainy = "64"
br_Cold = "64"
br_Windy = "100"

# Duration / Speed of the LED Switch
dur_Warm = "7000"
dur_Clear = "8000"
dur_Rainy = "1000"
dur_Cold = "5000"
dur_Windy = "2000"

# Color Palettes
no_Pal = "0"
RGB_Pal = "1"
rainbow_Pal = "2"
party_Pal = "3"
heat_Pal = "4"
fire_Pal = "5"
Cold_Pal = "6"

# Necessary Data for the weather API
API = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = ""
PARAMS = {"q": "YOUR_CITY", "units": "imperial", "APPID": API_KEY}

os.system("cls")
port = None

# Automatically finds all USB Ports on your Device
# Scans and connects to the Arduino Port eventually
def getPort():
	print("Listing all Ports:")
	port = None
	ports = serial.tools.list_ports.comports()
	for p in ports:
		print(p)
		if "Arduino" in p[1]:
			port = p[0]
			print("[+] Found Arduino Port:", port)
	return port

while(port==None):
	port = getPort()
	if port==None:
		print("[-] Failed to find an connected Arduino.\nRetrying in 5 seconds..")
		time.sleep(5)
	try:
		arduino = serial.Serial(port, 9600, timeout=1)
		print(f"[+] Successfully connected with Port {port}")
	except:
		print("[-] Failed to find an connected Arduino.\nRetrying in 5 seconds..")
		time.sleep(5)
		pass

# Hier beginnt die Magie
def trackWeather():
	resp = requests.get(API, params=PARAMS)
	print(resp.json())
	weather = resp.json()['weather'][0]['main']
	fahrenheit = round(resp.json()['main']['temp'])
	celcius = round((fahrenheit - 32) * .5556) # Converting the Fahrenheit to Celcius
	if weather == "Clouds" and celcius < 10:
		sendData("B=" + br_Cold)
		sendData("D=" + dur_Cold)
		sendData("C=" + coldColor)
		sendData("P=" + Cold_Pal)
		sendData("A=" + ani_Cold)
	elif weather == "Clouds" and celcius < 20:
		sendData("B=" + br_Clear)
		sendData("D=" + dur_Clear)
		sendData("P=" + Cold_Pal)
		sendData("A=" + ani_Cloudy)
	elif weather == "Clear":
		sendData("B=" + br_Clear)
		sendData("D=" + dur_Clear)
		sendData("C=" + clearColor)
		sendData("A=" + ani_Clear)
	elif weather == "Rainy":
		sendData("B=" + br_Rainy)
		sendData("D=" + dur_Rainy)
		sendData("C=" + rainyColor)
		sendData("A=" + ani_Rainy)
	elif weather == "Sun" and celcius < 20:
		sendData("B=" + br_Warm)
		sendData("D=" + dur_Warm)
		sendData("C=" + warmColor)
		sendData("A=" + ani_Warm)
	elif weather == "Sun" and celcius < 30:
		sendData("B=" + br_Warm)
		sendData("D=" + dur_Warm)
		sendData("P=" + heat_Pal)
		sendData("A=" + ani_Warm)
	else:
		print("The API responded with an unofficial weather value. Please open a Pull Request! :)")
	print(f"The weather is {weather} with {celcius}°C")

def awaitResponse(s):
    time.sleep(.1)
    while (s.in_waiting > 0):
        print(s.readline().decode(), end="")

def sendData(s):
    arduino.flush()
    s = s+'\n'
    arduino.write(s.encode())
    awaitResponse(arduino)
    time.sleep(.1)
    arduino.flush()

def main():
	while True:
		try:
			time.sleep(600)
			trackWeather()
		except Exception as exc:
			print(f"[{datetime.datetime.now()}] - Error: {exc}")
			sendData("C=FF0000")
			sendData("B=200")
			sendData("D=10")
			sendData("P=0")
			sendData("A=101")

if __name__ == '__main__':
	main()
