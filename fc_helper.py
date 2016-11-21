def fc3():


	start_address = input("Please enter starting address: ")
	length = input("Please enter number of registers to read: ")

	#Convert to hex with a 4 byte padding length
	hstart_address = "{0:0{1}x}".format(int(start_address)-1,4)
	hlength = "{0:0{1}x}".format(int(length),4)

	data = str(hstart_address)+str(hlength)

	return data

def fc6():

	try:
		start_address = input("Please enter address of regsiter to write to: ")
		value = input("Please enter value to write to register: ")

		#Convert to hex with a 4 byte padding length
		hstart_address = "{0:0{1}x}".format(int(start_address)-1,4)
		hvalue = "{0:0{1}x}".format(int(value),4)

		data = str(hstart_address)+str(hvalue)

		return data
	except Exception as e:
		print ('-! FC6 Error')
		print (str(e))
