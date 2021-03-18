import network
import time
from config import secrets, packages
import upip

ssid = secrets['SSID']
passwd = secrets['PASS']

def wifi_connect(ssid, passwd):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, passwd)
        time.sleep(1)
        while not wlan.isconnected():
            pass
    #set dns
    n = wlan.ifconfig()
    print(n)
    new_dns = (n[0], n[1], n[2], '8.8.8.8')
    wlan.ifconfig(new_dns)
    print('network config:', wlan.ifconfig())

def install_packages(packages):
    for package in packages:
        try:
            __import__(package)
            print("Successfully imported ", package, '.')
        except ImportError:
            upip.install(package)
            print('Installed ', package, '.')

wifi_connect(ssid, passwd)
