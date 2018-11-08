import serial

def pacemaker_serial_comm():
	pacemaker_inputs = "stuff from DCM"

	try: 
		ser = serial.Serial("COM3", baud_rate = 115200, bytesize=serial.SEVENBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_EVEN, timeout=1) 
		ser.close() 
		ser.open() 
		ser.write(pacemaker_inputs)
		# read_egram = serial.read(size=?)

		# print read_egram
		# if read_egram is not '':
		# 	print port 
	except(serial.SerialException):
		print("Device cannot be found or cannot be configured..")

if __name__ == '__main__':
	pacemaker_serial_comm()