import network
import time
import machine
from modules import LED
import sys
import logging


led_module = LED("LED")

from power_up_record import last_power_up
print('last_power_up =',last_power_up)

for i in range(4):
            led_module.toggle()
            time.sleep(.02)
            led_module.toggle()
            time.sleep(.1)

with open('power_up_record.py','w') as file:
            file.write("last_power_up = 'clean'")
with open('picoweb_mode.py','w') as file:
            file.write("mode = 'ap'")

def setup_ap():
    ssid = 'K.sysPicoW_AP'
    password = '12345678'  # Set your desired password or leave it empty for no password

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while ap.active() == False:
        pass

    print('Access point setup complete')
    print('SSID:', ssid)
    print('IP address:', ap.ifconfig()[0])
logging.info('>last_power_up', last_power_up)
    
def main():
    setup_ap()
    # You can add additional startup code here

if __name__ == "__main__":
    main()

