from machine import Pin

class LED:
    """This will represent our LED"""
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.led_pin = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        return self.led_pin.value()
    
    def toggle(self):
        self.led_pin.value(not self.get_value())

class Module0:
    """This will represent our module0"""
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.module0 = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        return self.module0.value()
    
    def toggle(self):
        self.module0.value(not self.get_value())

class Module1:
    """This will represent our module1"""
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.module1 = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        return self.module1.value()
    
    def toggle(self):
        self.module1.value(not self.get_value())

class Module2:
    """This will represent our module2"""
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.module2 = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        return self.module2.value()
    
    def toggle(self):
        self.module2.value(not self.get_value())

class Module3:
    """This will represent our module3"""
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.module3 = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        return self.module3.value()
    
    def toggle(self):
        self.module3.value(not self.get_value())

class Module4:
    """This will represent our module4"""
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.module4 = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        return self.module4.value()
    
    def toggle(self):
        self.module4.value(not self.get_value())

class Module5:
    """This will represent our module5"""
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.module5 = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        return self.module5.value()
    
    def toggle(self):
        self.module5.value(not self.get_value())

class Module6:
    """This will represent our module6"""
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.module6 = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        return self.module6.value()
    
    def toggle(self):
        self.module6.value(not self.get_value())

class Module7:
    """This will represent our module7"""
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.module7 = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        return self.module7.value()
    
    def toggle(self):
        self.module7.value(not self.get_value())

class Module8:
    """This will represent our module7"""
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.module8 = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        return self.module8.value()
    
    def toggle(self):
        self.module8.value(not self.get_value())

class Module9:
    """This will represent our module9"""
    
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.module9 = Pin(self.pinNumber, Pin.OUT)
        
    def get_value(self):
        return self.module9.value()
    
    def toggle(self):
        self.module9.value(not self.get_value())
