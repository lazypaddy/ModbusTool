***********************************************************

This is a tool written to work with Modbus and the command line
This is very much a work in progress and I will update as I go

Kudos to Mark Bristow (modscan.py) for a lot of the fundamentals of this code
***********************************************************

This is for use with Python 3 due to some of the methods required to run this programme
For help run:

modbus.py -h

Modbus Command Line Utility.  

Options:  
--version             				show program's version number and exit  
-h, --help            				show this help message and exit  
-p PORT, --port=PORT  				modbus port DEFAULT:502  
-t TIMEOUT, --timeout=TIMEOUT 		socket timeout (mills) DEFAULT:500  
-f FUNCTION, --function=FUNCTION	MODBUS Function Code DEFAULT:17  
--data=FDATA          MODBUS Function Data.  String Data " 00 01"  
-d, --debug           returns extremely verbose output  
-c, --continious      Continuously read registers  
-s SID, --sid=SID     Optional - Set SID for Modbus Slave (default=11)  
-i, --investigate     Optional - Scan for live devices  