from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from modules import LED, Module0, Module1, Module2, Module3, Module4, Module5, Module6, Module7, Module8, Module9
import network
import time
from microdot_websocket import with_websocket
from machine import Pin,ADC,Timer,reset
from netview import pico_esn,ifconf,apscan,pico_mac,aprssi,pico_esn
from adc_temp import Temp
import ujson
import json
import random
import logging
from logging import datetime_string
import ntp
import uasyncio as asyncio

# ----------------------------------------------------------------------------

print()
print("=======================================================================")
print()


def setup_ap():
    ssid = 'K.sysPicoW_AP'
    password = '12345678'  # Set your desired password or leave it empty for no password

    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
       # Optionally set a static IP address
    ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    
    # Attempt to activate the access point
    attempt = 0
    while not ap.active() and attempt < max_attempts:
        print(f'Attempt {attempt + 1} to activate AP...')
        time.sleep(1)
        attempt += 1

    # Check if access point was successfully activated
    if ap.active():
        print('Access point setup complete')
        print('SSID:', ssid)
        print('IP address:', ap.ifconfig()[0])
        return True
    else:
        print('Failed to activate access point')
        return False

ifconfig=ifconf()
ip=ifconfig[0]
# define timer_0 callback 
tim = Timer()
def tick(timer):
    print('timer_0 ran out')
    delayed_reboot()
# tim.init(period=300000, mode=Timer.ONE_SHOT, callback=tick) # 5 minutes
# tim.init(period=900000, mode=Timer.ONE_SHOT, callback=tick) # 15 minutes
tim.init(period=1200000, mode=Timer.ONE_SHOT, callback=tick) # 20 minutes
# load one time variables
logging.debug('> IP', ip)
logging.debug('> APSCAN', apscan())
logging.debug('ifconf:', ifconf())
logging.debug('NTP:', ntp.fetch(synch_with_rtc=True, timeout=10))  # sync to ntp and log 
start_time=datetime_string()
# grab at startup only  
print()
print("=======================================================================")
print()
global_data = {'variable1': 0, 'variable2': 0, 'variable3': 0}

app = Microdot()
Response.default_content_type = 'text/html'
# Our LED Module
led_module = LED("LED")
module0 = Module0(0)
module1 = Module1(1)
module2 = Module2(2)
module3 = Module3(3)
module4 = Module4(4)
module5 = Module5(5)
module6 = Module6(6)
module7 = Module7(7)
module8 = Module8(8)
module9 = Module9(9)
ADC0 = ADC(0)
ADC1 = ADC(1)
ADC2 = ADC(2)

pins = {
    1: machine.Pin(1, machine.Pin.OUT),
    2: machine.Pin(2, machine.Pin.OUT),
    3: machine.Pin(3, machine.Pin.OUT),
    4: machine.Pin(4, machine.Pin.OUT),
    5: machine.Pin(5, machine.Pin.OUT),
    6: machine.Pin(6, machine.Pin.OUT),
    7: machine.Pin(7, machine.Pin.OUT),
    8: machine.Pin(8, machine.Pin.OUT),
    9: machine.Pin(9, machine.Pin.OUT)
}
def save_states():
    states = {pin_num: pin.value() for pin_num, pin in pins.items()}
    with open('gpio_states.json', 'w') as f:
        json.dump(states, f)
def blink(tim):
    for i in range(2):
            led_module.toggle()
            time.sleep(.02)
            led_module.toggle()
            time.sleep(.02)
def get_slow_stuff():
    global temp2, rssi 
    temp2=str(Temp())  #  .7 second read time
    rssi=str(aprssi()) #  .5 second read time  
get_slow_stuff()

pin_schedule = {}
gpio_pins = [Pin(i, Pin.OUT) for i in range(9)]  # Assuming 3 GPIO pins for demonstration

def schedule_gpio(pin, on_time, off_time):
    """Schedules GPIO pin to turn on and off at specified times."""
    pin_schedule[pin] = {'on_time': on_time, 'off_time': off_time}
    print(f"Scheduled GPIO {pin} ON at {on_time} and OFF at {off_time}")

def get_time():
    current_time = time.localtime()
    hours = current_time[3]
    minutes  = current_time[4]
    return (hours, minutes)
   

async def gpio_control():
    """Controls GPIO pins based on the schedule."""
    while True:
        current_window = get_time()
        print( current_window)
        for pin, schedule in pin_schedule.items():
            if schedule['on_time'] <= current_window <= schedule['off_time']:
                gpio_pins[pin].value(1)
                print("relay", [pin], "on")
            else:
                gpio_pins[pin].value(0)
                print("relay", [pin], "off")
        await asyncio.sleep(10)
        
@app.route('/switchscheduler')
async def index(request):
    return render_template('switchscheduler.html')

@app.route('/schedule', methods=['POST'])
async def set_schedule(request):
    data = request.json
    pin = int(data['pin'])
    on_time = tuple(map(int, data['on_time'].split(':')))
    off_time = tuple(map(int, data['off_time'].split(':')))
    schedule_gpio(pin, on_time, off_time)
    return ujson.dumps({'status': 'success', 'schedule': pin_schedule})

@app.route('/get_schedule')
async def get_schedule(request):
    return ujson.dumps(pin_schedule)

adcs = [machine.ADC(26), machine.ADC(27), machine.ADC(28)]

@app.route('/updateAdcData')
def update_adc_data(request):
    pin = int(request.args.get('pin', '0'))
    if pin < 1 or pin > 9:
        return Response(status_code=400, text="Invalid pin number")

    adc_value = adcs[pin - 1].read_u16() * 3.3 / 65535  # Convert to voltage
    return {'adcValue': adc_value}
@app.route('/')
async def index(request):
    return render_template('index.html')
@app.route('/iframeswitches')
async def index(request):
    return render_template('iframeswitches.html')
@app.route('/iframeswitches2')
async def index(request):
    return render_template('iframeswitches2.html')
@app.route('/switchLED')
async def index(request):
    return render_template('switchLED.html', led_value=led_module.get_value())
@app.route('/switch0')
async def index(request):
    return render_template('switch0.html', module0_value=module0.get_value())
@app.route('/switch1')
async def index(request):
    return render_template('switch1.html', module1_value=module1.get_value())
@app.route('/switch2')
async def index(request):
    return render_template('switch2.html', module2_value=module2.get_value())
@app.route('/switch3')
async def index(request):
    return render_template('switch3.html', module3_value=module3.get_value())
@app.route('/switch4')
async def index(request):
    return render_template('switch4.html', module4_value=module4.get_value())
@app.route('/switch5')
async def index(request):
    return render_template('switch5.html', module5_value=module5.get_value())
@app.route('/switch6')
async def index(request):
    return render_template('switch6.html', module6_value=module6.get_value())
@app.route('/switch7')
async def index(request):
    return render_template('switch7.html', module7_value=module7.get_value())
@app.route('/switch8')
async def index(request):
    return render_template('switch8.html', module8_value=module8.get_value())
@app.route('/switch9')
async def index(request):
    return render_template('switch9.html', module9_value=module9.get_value())

@app.route('/updateData')
async def get_sensor_data(request):
    print("Receive get data request!")
    get_slow_stuff()
    sensor_reads_alt = random.uniform(200, 300)
    randHum = random.uniform(10, 30)
    randpress = random.uniform(100, 200)
    randAlt = random.uniform(220, 300)
    print(sensor_reads_alt)
    print("temp", temp2)
    print(rssi)
    return ujson.dumps({"readingTemp": temp2, "readingHum": randHum, "readingPress": randpress, "readingAlt": randAlt})

@app.route('/updateNoise')
async def get_ds18b20_reads(request):
    print("Receive get values request!")
    sensor_reads_noise = random.uniform(100, 30)#ds_sensor.get_noise_reading()
    return ujson.dumps({"readingNoise" : sensor_reads_noise})
# replace with actual code to read from a sensor@app.route('/metrics')
def get_metrics(request):
    # Dummy data for metrics
    metrics = [
        {'ssid': 'Network1', 'ip': '192.168.1.1', 'location': 'Office', 'apName': 'AP1', 'otherMetrics': 'Metric1'},
        {'ssid': 'Network2', 'ip': '192.168.1.2', 'location': 'Home', 'apName': 'AP2', 'otherMetrics': 'Metric2'}
    ]
    return ujson.dumps(metrics)
@app.route('/pinstate')
def get_pin_state(request):
    pin_number = request.args.get('pin', '')
    state = pin.get(pin_number, {'state': 'N/A'})
    return ujson.dumps(state)
@app.route('/LED')
async def toggle_led(request):
    print("Receive LED Toggle Request!")
    led_module.toggle()
    return "OK"
@app.route('/module0')
async def module0_toggle(request):
    print("Receive module0 Toggle Request!")
    module0.toggle()
    return "OK"
@app.route('/module1')
async def module1_toggle(request):
    print("Receive module1 Toggle Request!")
    module1.toggle()
    return "OK"
@app.route('/module2')
async def module2_toggle(request):
    print("Receive module2 Toggle Request!")
    module2.toggle()
    return "OK"
@app.route('/module3')
async def module3_toggle(request):
    print("Receive module3 Toggle Request!")
    module3.toggle()
    return "OK"
@app.route('/module4')
async def module4_toggle(request):
    print("Receive module4 Toggle Request!")
    module4.toggle()
    return "OK"
@app.route('/module5')
async def module5_toggle(request):
    print("Receive module5 Toggle Request!")
    module5.toggle()
    return "OK"
@app.route('/module6')
async def module6_toggle(request):
    print("Receive module6 Toggle Request!")
    module6.toggle()
    return "OK"
@app.route('/module7')
async def module7_toggle(request):
    print("Receive module7 Toggle Request!")
    module7.toggle()
    return "OK"
@app.route('/module8')
async def module8_toggle(request):
    print("Receive module8 Toggle Request!")
    module9.toggle()
    return "OK"
@app.route('/module9')
async def module9_toggle(request):
    print("Receive module9 Toggle Request!")
    module9.toggle()
    return "OK"
@app.route('/metrics')
async def index2(request):
    return render_template('metrics.html')
@app.route('/ADCmetrics')
async def index2(request):
    return render_template('ADCmetrics.html')
@app.route('/switchboard')
async def index2(request):
    return render_template('switchboard.html')
@app.route('/VeriableKeyIn')
async def index2(request):
    return render_template('variables.html')
# Route to serve the HTML form
@app.route('/manual')
async def index2(request):
    return render_template('manpage.html')
# Route to handle POST request from the forms
@app.route('/submit', methods=['POST'])
def submit(request):
    global global_data
    try:
        data = ujson.loads(request.body)  # Parse the JSON payload
        for key in data:
            if key in global_data:
                global_data[key] = int(data[key])
                logging.debug('> global data recieved')
        return 'Data received and stored successfully', 200
        
    except Exception as e:
        return f'Error: {str(e)}', 400
# Route to display the stored data (for testing/debugging)
@app.route('/data', methods=['GET'])
def get_data(request):
    global global_data
    return ujson.dumps(global_data)
# Route to serve the HTML form
@app.route('/logs')
async def index2(request):
    return send_file('log.txt')
@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'
@app.route('/static/<path:path>')
def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)

tim.init(period=600000, mode=machine.Timer.PERIODIC, callback=lambda t: save_states())
tim.init(period=100000, mode=Timer.PERIODIC, callback=blink)

async def main():
    asyncio.create_task(gpio_control())
    await app.start_server(port=5000, debug = True)

try:
    asyncio.run(main())
except Exception as e:
    print(f"Error: {e}")

