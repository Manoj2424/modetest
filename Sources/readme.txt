* IP Validation ReadMe File for Display *
-------------------------------------

Execution (To run complete (sanity and automated) test suite):
-------------------------------------------------------------

Run the ip_validate.sh file in the terminal as below:
	
sanity    : It contains the basic Display test case.
	    (Sanity Test Cases: 1)

	  sudo ./ip_validate.sh -n disp -o '-t sanity'

-> This command executes the sanity Test, and the result gets logged to the console.
 
automated : It contains automated test case for the Display.
            (Automated Test Cases: 2, 7, 8, 10)
 
 	   sudo ./ip_validate.sh -n disp -o '-t automated'

-> This command executes the automated Test, and the result gets logged to the console.

manual : It contains manual test case for the Display.
            (Manual Test Cases: 3, 4, 5, 6, 9)
 
 	   sudo ./ip_validate.sh -n disp -o '-t manual'

-> This command executes the Manual Test, and the result gets logged to the console.
	
Execute the python test case (individual):
-----------------------------------------

* Total Test Case in python : 14 

Run the python test case:
	sudo ./ip_validate.sh -n disp -o '-t 4'

-> This command executes the 4th Test, and the result gets logged to the console.

Usage:
------

Usage: ./ip_validate.sh [options]

-n 	       - Name of the IP.
-o <test_opts> - Test options specific to the IP under test to be passed for running the test.	
		 This option is applicable only for running the test and not applicable for build and install.
-h             - Display this help information.
-t             - test case number.
	Example : -t 1 // Only Takes integer	


Folder Contains:
---------------

* common : Contains Test utilities, & common header files.
* disp    : IP Validation folder which contains Makefiles, main test_disp.py file, & other binaries.
* logs   : Conatins the executed logs files.


Author:
------
Ramesh K P
Exaleap Semiconductor Pvt Ltd. 

Ramesh K P
Exaleap Semiconductor Pvt Ltd. 
