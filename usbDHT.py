import serial
import time
import os

class DHT ():      
   def findUsbDevice (self, response):
      ls = os.popen ( 'ls /dev/ttyUSB*').read()  
      lines = ls.split ( '\n')
      port = ''
      for line in lines:
         if port != '':
            break
         if line.strip() != '':
            portName = line.strip()
            try: 
               comPort = serial.Serial (portName, 57600, timeout = 0.01)
               startTime = time.time()
               while time.time() < startTime + 3:
                  line = comPort.readline () 
                  if line.strip() != '':
                     if line.strip() == expectedResponse:
                        print 'Found expected response on port: ' + port 
                        port = portName
                     break
               comPort.close()
            except Exception as inst:
               print 'Err: ' + str(inst)             
            if port == '':
               print 'Could not find device with response: ' + response
            else:               
               print 'Found device at port: ' + port 
      self.portName = port      
      return port 
      
   
   def readDHT (self):
      comport = serial.Serial (self.portName, 115200, timeout = 0.01)
      # read the response 
      startTime = time.time()
      while time.time() < startTime + 3:
         line = comport.readline()
      comport.write ( '?')
      startTime = time.time()
      currentTime = ''
      while time.time() < startTime + 3:
         line = comport.readline()
         if line.strip() != '':
            break
      comport.close()      
               
      return line
      
   def fahrenheit (self):
      line = self.readDHT()
      index = line.find ('*F')
      value = ''
      if index > -1:
         startIndex = line.rfind ( ' ',0, index-2)
         value = line [startIndex+1:index-1]
      print value
      return float(value)
      
   def celcius (self):
      line = self.readDHT()
      index = line.find ('*C')
      value = ''
      if index > -1:
         startIndex = line.rfind ( ' ',0, index-2)
         value = line [startIndex+1:index-1]
      print value
      return float(value)
      
   def humidity(self):
      line = self.readDHT()
      index = line.find ('%')
      value = ''
      if index > -1:
         startIndex = line.rfind ( ' ',0, index-2)
         value = line [startIndex+1:index-1]
      print value
      return float(value)
     
   def heatIndex(self):     
      line = self.readDHT()
      index = line.find ('Heat index:')
      value = ''
      if index > -1:
         startIndex = index + 11
         index = line.find ( '*C', startIndex + 1)
         value = line [startIndex+1:index-1]
      print value
      return float(value)
         
if __name__ == '__main__':
   dht = DHT()
   # For Windows
   dht.portName = 'com4'
   
   #For Raspberry Pi: 
   #port = dht.findUsbDevice ('DHTR')
   
   #print dht.readDHT ()
   dht.fahrenheit () 
   dht.celcius()
   dht.humidity()
   dht.heatIndex()
