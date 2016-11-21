#!/usr/bin/env python

"""
File: modbus.py
Desc: Modbus TCP Helper
Version: 0.1

Copyright (c) 2016 John Wiltshire

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version either version 3 of the License, 
or (at your option) any later version.


This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Resources:
http://www.simplymodbus.ca/TCP.htm
https://itunes.apple.com/us/app/modbus-server-pro/id618058292?mt=8
Kudos to Mark Bristow (modscan.py) for a lot of the fundamentals of this code
"""

import socket
import optparse
from IPy import IP
import sys
import fc_helper
import mb_helper
import time

def main():

	p = optparse.OptionParser(	description=' Modbus Command Line Utility.',
								prog='modbus',
								version='modbus 0.1',
								usage = "usage: %prog [options] IPRange")
	p.add_option('--port', '-p', type='int', dest="port", default=502, help='modbus port DEFAULT:502')
	p.add_option('--timeout', '-t', type='int', dest="timeout", default=500, help='socket timeout (mills) DEFAULT:500')
	p.add_option('--function', '-f', type='int', dest="function", default=17, help='MODBUS Function Code DEFAULT:17')
	p.add_option('--data', type='string', dest="fdata", help='MODBUS Function Data.  String Data " 00 01"')
	p.add_option('-d', '--debug', action ='store_true', help='returns extremely verbose output')
	p.add_option('-c', '--continious', action ='store_true', help='Continuously read registers')
	p.add_option('-s', '--sid', type='int',dest='sid', default=11, help='Optional - Set SID for Modbus Slave (default=11)')
	p.add_option('--investigate', '-i', action = 'store_true', help='Optional - Scan for live devices')


	options, arguments = p.parse_args()

	msg = ''

	#Check we have at least 1 argument (IP Addresses

	if len(arguments) == 1:

		#assign IP range
		try:
			iprange=IP(arguments[0])
		

			mb = mb_helper.MBHelper()
			if options.fdata == None and options.function == 3:
				options.fdata = fc_helper.fc3()

			elif options.fdata == None and options.function == 6:
				options.fdata = fc_helper.fc6()

			mb.msg += 'fdata: ' + str(options.fdata) + ' \n'
			

			#start of for ip in iprange
			for ip in iprange:
				#print('Reading from %s' % ip)
				
				# ----------------- MB SCAN -----------------------
				if options.investigate:
					connected_devices = mb.mb_scan(str(ip), int(options.port))
					if connected_devices == False:
						print('Could not connect to %s' % ip)
					else:
						for item in connected_devices:
							print ('+ %s is alive' % item)
				
				# ---------------- MB FC --------------------------
				else:
					try:
						b_fdata = bytearray.fromhex(options.fdata)
						resp = mb.mb_send_cmd(str(ip), int(options.port), int(options.sid), int(options.function), str(options.fdata))
						if options.function == 3:
							
							if (int(resp[7]) == int(options.function)):
								mb.msg += 'FC3 Response... \n'

								start_addr = (b_fdata[0] * 256) +(b_fdata[1])	
								mb.msg += 'Start Address: ' + str(start_addr) + ' \n'
								for i in range(1,int(resp[8]),2):
									register = int(start_addr+((i+1)/2))

									print('Value for register %s : %s is' % (ip,register) , int(resp[8+i]*256)+int(resp[9+i]))
						elif options.function == 6:
							
							if (int(resp[7]) == int(options.function)):
								mb.msg += 'FC6 Response... \n'

								register = (b_fdata[0] * 256) +(b_fdata[1]+1)	
								mb.msg += 'Start Address: ' + str(register) + ' \n'

								print('Value for register %s : %s is' % (ip,register) , int(resp[10]*256)+int(resp[11]))
						else:	
							print('Unknown FC Response: ' + str(resp))

					except Exception as e:
						print('Could not connect to %s' % ip)
						print (str(e))
						#print mb.msg

		except Exception as e:
			print ('Main Loop Error')
			print (str(e))
			print('-------------Staring Debug------------')
			print(mb.msg)
			print('-------------End Debug------------')			

		#end of for ip in iprange
		
		#print debug messages
		if options.debug:
			print('-------------Staring Debug------------')
			print(mb.msg)
			print('-------------End Debug------------')




if __name__ == '__main__':
	try :
		req_version = (3,0)
		cur_version = sys.version_info

		if cur_version >= req_version:
			main()
		else:
		   print ("Your Python interpreter is too old. Please consider upgrading. \n Must be greater than Python Version {}.{}".format(req_version[0], req_version[1]))
		
	except KeyboardInterrupt:
		print("Scan canceled by user.")
		print("Thank you for using Modbus Tool")
	except :
		sys.exit()
		

	