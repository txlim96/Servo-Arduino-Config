import serial
import sys
import glob
import time

def listSerialPorts():
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.usbserial-*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        result.append(port)
#    for port in ports:
#        try:
#            s = serial.Serial(port)
#            s.close()
#            result.append(port)
#        except (OSError, serial.SerialException):
#            pass
    return result

def setupSerial(serPort):
    global ser
	
	# NOTE the user must ensure that the serial port and baudrate are correct
	#~ serPort = "/dev/ttyS81"
    baudRate = 9600
    ser = serial.Serial(serPort, baudRate, timeout=1)
    return ser
#	print("Serial port " + serPort + " opened  Baudrate " + str(baudRate))

def closeSerial():
    global ser
    try:
        ser.__del__()
    except Exception as e:
        print(e)
        pass

def sendData(idx, val):
    print("sending...")
    try:
        ser.write('<'.encode('utf-8'))
        ser.write(idx.encode('utf-8'))
        ser.write(':'.encode('utf-8'))
        ser.write(val.encode('utf-8'))
        ser.write('>'.encode('utf-8'))
        
        time.sleep(0.5)
        print("ready")
    except Exception as e:
        print(e)
        pass

def testServo(idx):
    print("sending")
    try:
        ser.write('<'.encode('utf-8'))
        ser.write(idx.encode('utf-8'))
        ser.write('>'.encode('utf-8'))

        time.sleep(0.5)
        print('ready')
    except Exception as e:
        print(e)
        pass
        
##port = listSerialPorts()[0]
##setupSerial(port)

##try:
##    while (True):
##        var = input("Please enter: ")
##        ser.write('<'.encode('utf-8'))
##        ser.write(var.encode('utf-8'))
##        ser.write('>'.encode('utf-8'))
##except KeyboardInterrupt:
##    closeSerial()
