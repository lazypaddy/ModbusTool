import socket
from IPy import IP

class MBHelper:

	#rsid = array.array('B')
	msg = ''
	rsid = ''

	def __init__(self):
		#build basic packet
		"""
		Modbus Packet Structure
		\x00\x00	\x00\x00	\x00\x00	\x11		\x00		<=================>
		Trans ID	ProtoID(0)	Length		UnitID		FunctCode	Data len(0-253byte)
		"""
		self.rsid = '00 00 00 00 00 02 00 01'

	def __del__(self):
		try:
			self.s.close()
		except:
			pass

	def mb_connect(self, ip, port, timeout=500):

		self.port = port
		self.timeout = timeout

		try:
			#socket object instantiation
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			#set socket timeout, value from cmd is in mills
			self.s.settimeout(float(self.timeout) / float(1000))			

			#connect requires ip addresses in string format so it must be cast
			self.msg += 'Connecting ... \n'
			self.s.connect((str(ip), self.port))
			self.msg += 'Connected to: %s \n' % str(ip)
			return True
		

		except socket.error:
			#clean up
			self.msg += 'Failed to connect to: %s \n' % str(ip)
			return False
			self.s.close()

		#end try

	def mb_scan(self, ip, port, sid_low = 1, sid_high = 247):
		
		connected_devices = []


		if not self.mb_connect(ip, port):
			return False

		self.msg += '+ Connected to %s \n' % str(ip)
		adu = bytearray.fromhex(self.rsid)

		connected_devices.append(str(ip))

		#loop over possible sid values
		for sid in range (sid_low, sid_high):	
			self.msg += ' Testing %s SID \n' % str(sid)
			#send query to device
			try:
				#set slave id
				adu[6]=sid		

				#send data to device
				self.msg += 'ADU Sent: ' + str(type(adu)) + ' : ' + str(adu) + '\n'
				self.s.send(adu)

			except socket.error:
				#failed send close socket
				self.msg += str(sid) + ": FAILED TO SEND\n"
				break
			#end try
			
			try:
				#recieve data
				data = self.s.recv(1024)
				
			except socket.timeout:
				self.msg += str(sid) + ": FAILED TO RECV\n"
				break
			#end try

			#examine response
			if data:
				self.msg += 'Response: ' + str(data) + '\n'
				#parse response
				#if the function matches the one sent we are all good
				#print 'Response fcode: %s \t Requested fcode: %s' % (resp[7], options.function)
				if (int(data[7]) == int(adu[7])):
					connected_devices.append(str(ip) + ':' + str(sid))					
				#If the function matches the one sent + 0x80 a positive response error code is detected
				elif int(data[7]) == (int(adu[7])+128):
					#if debug output message
					self.msg += str(sid) + ": Positive Error Response\n"
								
			else:
				self. msg += str(sid) + ": FAILED TO RECIEVE\n"
		
		self.s.close()
		return connected_devices	
		#end SID for

	def mb_send_cmd(self, ip, port, sid, pdu_fc, pdu_data):
		
		if not self.mb_connect(ip, port):
			self.msg += '-! Connection Error'
			return False

		#send query to device
		try:
			byte_pdu_data = bytearray.fromhex(pdu_data)
			self.msg += 'PDU' + str(type(byte_pdu_data)) + ' : ' + str(byte_pdu_data) + '(string data: ' + pdu_data + ')\n'

			#set slave id
			adu = bytearray.fromhex(self.rsid)

			adu[6] = int(sid)
			adu[7] = int(pdu_fc)

			self.msg += 'RSID: ' + str(type(adu)) + ' : ' + str(adu) + '\n'

			adu += byte_pdu_data

			#update length
			adu[5]=len(byte_pdu_data)+2	
			self.msg += 'ADU Sent: ' + str(type(adu)) + ' : ' + str(adu) + '\n'
			#send data to device
			self.s.send(adu)

			#recieve data
			data = self.s.recv(1024)

			if data:
				#parse response
				self.msg += 'Response: ' + str(type(data)) + ' : ' + str(data) + '\n'

				if (int(data[7]) == pdu_fc):
					return data						
				else:
					#return None
					return data				
			else:
				return None

			self.s.close()
		except Exception as e:
			print (str(e))
