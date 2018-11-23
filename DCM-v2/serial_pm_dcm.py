import serial

def pacemaker_serial_comm(info):

	try: 
		ser = serial.Serial("COM5", 115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, timeout=0) 
		ser.close() 
		ser.open() 
		ser.write(info)
		read_egram = ser.read(size=23)

		print("Received: ", read_egram)
		# if read_egram is not '':
		# 	print port 
	except(serial.SerialException):
		print("Device cannot be found or cannot be configured..")

if __name__ == '__main__':
	pacemaker_serial_comm()


#pin = D9 (vent_pace_ctrl) PTC4 
# info_bytes = 4 - 21 
# data_size = 23
