""" Powers a minecraft server control cube
Behavior: Cube light is dim red to start (redstone block). If someone presses the 'on' button,
The cube will begin to slowly pulse green (emerald block). The program will request the
start of the server then check periodically to see if the server is reachable. Once it
returns an 'on' response, the cube will display a light blue (diamond). When the off
button is pressed, the cube will pulse red until the server no longer responds to
requests. At that point the cube will switch to red."""

from config import colors, secrets, debug, buttons, neopixels
from machine import Pin, Timer
from micropython import schedule
import neopixel
import time
import urequests
import usocket

## SETUP
np = neopixel.NeoPixel(Pin(neopixels['pin']), neopixels['pixels'])
on_button = Pin(buttons['on'], Pin.IN, Pin.PULL_UP)
off_button = Pin(buttons['off'], Pin.IN, Pin.PULL_UP)
server_status_timer = Timer(0)
# set_light_timer = Timer(1)

def set_light_color(color):
    for l in range(neopixels['pixels']):
        np[l] = color
    np.write()
    # check if lights change?
    return True


def start_server():
    """ GET HTTP request ot logic app endpoint defined in config 
    
    This needs work. Light should pulse when server is changing
    state.
    """
    set_light_color(colors['SERVER_START'])
    if debug == True:
        print("Debugging mode. Skipping server start.")
        time.sleep(3) # Keep the light green for 3 seconds
        return True
    else:
        urequests.get(secrets['START_SERVER_URL'])
        while not server_online: 
            time.sleep(10)
            set_server_status()
        set_light_to_server_status(server_online)
        return True


def stop_server():
    """ GET HTTP request to logic app endpoint defined in config """
    set_light_color(colors['SERVER_STOP'])
    if debug == True:
        print("Debugging mode. Skipping server stop.")
        time.sleep(3) # Keep the light red for 3 seconds
        return True
    else:
        urequests.get(secrets['STOP_SERVER_URL'])
        while server_online:
            time.sleep(10)
            set_server_status()
            # pulse LED here
        set_light_to_server_status(server_online)
        return True


def check_server_status():
    """Check the server to see if it is running by connecting to the port"""
    if debug == True:
        print("Checking if the server is Online")
    try:
        s = usocket.socket()
        s.settimeout(1.0) #TODO: move timeout to config
        s.connect( (secrets['SERVER_IP_ADDRESS'], 25565) ) # TODO: server port to config
        s.close()
        if debug == True:
            print("Server Online")
        return True
    except OSError as err:
        s.close()
        if debug == True:
            print("Error" + str(err))
        if str(err) == "[Errno 103] ECONNABORTED" or "[Errno 113] EHOSTUNREACH":
            if debug == True:
                print("Server Offline")
            return False
        else:
            if debug == True:
                print("Error" + str(err))
            return None

def set_server_status():
    global server_online
    server_online = check_server_status()


def button_press(button, threshold):
    count = button.value()
    while count <= threshold:
        if button.value() == 0:
            return False
        count += button.value()
        if count == threshold:
            time.sleep(.5)
            return True


def set_light_to_server_status(status):
    if debug == True:
        print("Setting light to server status.")
    
    if status:
        if debug == True:
            print("Setting to diamond")
        set_light_color(colors['SERVER_RUNNING'])
    elif status == False:
        if debug == True:
            print("Setting to light to gold")
        set_light_color(colors['SERVER_OFFLINE'])
    else:
        print('Failed to get server status.')
        set_light_color((100, 100, 100))


server_online = check_server_status()
# Get the status once at startup
set_light_to_server_status(server_online)
# Set a timer to get status periodically
#TODO move 'period' to config
server_status_timer.init(
        period=180000,
        mode=Timer.PERIODIC,
        callback=schedule(set_server_status(), None)
        )

# Main loop
while True:
    #detect button presses
    if debug == True:
        print("On: " + str(on_button.value()) + " Off: " + str(off_button.value()))
    if on_button.value() == 1:
        press = button_press(on_button, 750)
        if press:
            print('successful on press')
            start_server()
    if off_button.value() == 1:
        press = button_press(off_button, 750)
        if press:
            print('successful off press')
            stop_server()
