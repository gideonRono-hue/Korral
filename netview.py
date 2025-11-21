def ifconf():
  import network
  wlan = network.WLAN(network.STA_IF)
  return wlan.ifconfig()

def apscan():
  import network
  wlan = network.WLAN(network.STA_IF)
  wlan.scan()
  return wlan.scan()

def aprssi():
  import network
  wlan = network.WLAN(network.STA_IF)
  # wlan.scan()
  try:
    scan = wlan.scan()
    rssi = (scan[0])[3]  # grab first rssi on list
  except:
    rssi = 0
  return rssi

def pico_mac():
  import ubinascii
  import network
  wlan = network.WLAN(network.STA_IF)
  mac = ubinascii.hexlify(wlan.config('mac'), ':').decode()
  return mac

def pico_esn():
  import ubinascii  
  # client_id = ubinascii.hexlify(machine.unique_id())
  client_id = ubinascii.hexlify(machine.unique_id(), ':').decode()
  return client_id

