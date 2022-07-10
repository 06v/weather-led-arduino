<h1 align="center">Weather Tracker - Arduino RGB LED Strip</h1>

<div align="center">
  <img src="https://media.discordapp.net/attachments/914194110330576906/995748567090216970/unknown.png?width=500&height=374" id="center">
  <p align="center">
    Created by <a href="https://enes.vip" target="_blank">Enes</a>
  </p>
</div>

## Using the Tool

First edit the "q" parameter to the City of your choice which shall be weather tracked.
```python
PARAMS = {"q": "YOUR_CITY", "units": "imperial", "APPID": API_KEY}
```

Lastly you will need to input your Openweather `API Key`. This is free.
```python
API = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = ""
```

That's needed in order to acces the Openweather API, we will retrieve our weather data through this.<br/>You will be running the script locally so the usage won't store your API key.

Optionally you can edit the interval in which the weather is tracked. Currently it's at 600 seconds -> 10 minutes.
```python
def main():
	while True:
		try:
			time.sleep(600)
			trackWeather()
		except Exception as exc:
      ...
```

## Features & how it works

Whilst the Arduino Port is equal to None - meaning not connected through USB - it will keep checking the USB Ports of our devices (Raspberry Pi, Laptop, PC) for new plug-ins.<br/> If the Arduino has been plugged in to the device, it will automatically establish a connection using the Port
```python
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
```

Our USB Ports are foud using the `"list_ports"` method of the serial library.
```python
ports = serial.tools.list_ports.comports()
	for p in ports:
		print(p)
		if "Arduino" in p[1]:
			port = p[0]
			print("[+] Found Arduino Port:", port)
	return port
```

Next, we send a request to the weather API. This will respond with data such as if the weather is cloudy, rainy, clear and so on.<br/> Fahrenheit is also returned, allthough I have converted it to celcius in the Python program.
```python
def trackWeather():
	resp = requests.get(API, params=PARAMS)
	print(resp.json())
	weather = resp.json()['weather'][0]['main']       # This is the weather status
	fahrenheit = round(resp.json()['main']['temp'])
	celcius = round((fahrenheit - 32) * .5556)        # Converting the Fahrenheit to Celcius
```

This is where the fun part begins: Sending the colors, animations, the brightness ect. accordingly to the weather to our Arduino.<br/>Feel free to play around with the values initialized at the very beginning.
```python
elif weather == "Clear":
		sendData("B=" + br_Clear)
		sendData("D=" + dur_Clear)
		sendData("C=" + clearColor)
		sendData("A=" + ani_Clear)
```

Finally, we have two functions so the Arduino knows what's going on. The sendData() function & the awaitResponse() function:
```python
def awaitResponse(s):
    time.sleep(.1)
    while (s.in_waiting > 0):                # The number of bytes in our input buffer
        print(s.readline().decode(), end="") # The Arduino side output

def sendData(s):
    arduino.flush()           # Waits for the transmission of outgoing serial data to complete
    s = s+'\n'                # We need a \n (new line) for any data we send, Arduino logic
    arduino.write(s.encode()) # Writes over our encoded data (B, D, C, A, P) in bytes
    awaitResponse(arduino)    # Awaits the respsonse of our Arduino
    time.sleep(.1)
    arduino.flush()
```

<img src="https://media.discordapp.net/attachments/914194110330576906/995750084157386822/unknown.png" id="center">

## Related books
- [The ALA library](https://github.com/bportaluri/ALA)
- [The Openweather API](https://openweathermap.org/api)
