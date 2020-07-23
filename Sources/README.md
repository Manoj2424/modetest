## IP Validation ReadMe file for DISPLAY.

Python Modules and dependencies to Install:
==================================
    All the Dependencies can be installed via ./setup.sh file..

Packages :
===================
	The packages and other dependencies can be installed via direct shell file specified above, which does the work for you.. 

Test Suite Execution :
===================
	<Yet to Conclude on the below..>

    Total Test Cases added in the Framework (in Python) : 15
	
	Run the ip_validate.sh file in the Terminal as below:
	
	Single Test :  Parse the Test Number with -t <test_case> argument
		./ip_validate.sh -n disp -o '-t 1 -i 1'	

	Sanity : Test from 1, 2, 3 ,4, 5 are part of Sanity.
		./ip_validate.sh -n disp -o '-t sanity'

	Automated : Executes all tests in a single run.
		./ip_validate.sh -n disp -o '-t automated'

	The tests executes and the result gets logged to the console. And Test logs can be 
	available in logs/ folder for each test.
		
Usage : 
===================
		-n 				-	Name of the IP.
	 	-o <test_opts>  -	Test options specific to the IP under test to be passed for running the test."
    	                  	This option is applicable only for ruuning the test and not applicable for"
    	                   	build and install."
      	-b      	    -   Only build the binaries for specified IP or for all IPs (doesn't run test)."
      	-i  	        -   Only install the IP validation package for specified IP or for all IPs"
        	              	(doesn't run test)."
    	-h              -	Display this help information."


		-t				-	test case number.
				Example : -t 1 		//	Only Takes integer. 
		-i				-	test case iteration..
				Example : -i 5		// Executes Test for 5 Cycles, does only take integer. 
				

Folder Contains:
===================

		*	common 	:	Contains Test utilities, & common header files. 
		*	disp	:   IP Validation folder which contains Makefile, main test_gpu.py file, & other binaries. 
		*	logs	:	Contians the exeucted logs files. 
	

Author :
===================
		Ravi Kiran
		Exaleap Semi Confidential. 