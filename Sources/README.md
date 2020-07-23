## IP Validation ReadMe file for GPU.

Python Modules and dependencies to Install:
==================================
        ◦ Selenium with Webdriver. 		Install – pip3 install selenium
        ◦ Webdriver manager				Install – pip3 install webdriver_manager
        ◦ Psutil										Build-in Module
        ◦ OS											Build-in Module
        ◦ PyAutoGUI								Install – pip3 install pyautogui
        ◦ Subprocess							Build-in Module 
        ◦ Time										Build-in Module
        ◦ Logging									Build-in Module
        ◦ Cv2										Install – pip3 install pyopencv
        ◦ Sdl2										Install – pip3 install sdl2
        ◦ Vulkan									Install – pip3 install vulkan
        ◦ PyOpenGL								Install – pip3 install pyopengl
        ◦ Glfw										Install – pip3 install glfw
        ◦ PyOpenCL								Install – pip3 install pyopencl
        ◦ Scipy										Install – pip3 install scipy
        ◦ PyGame									Install – pip3 install pygame

Packages :
===================
	sudo apt-get install mesa-utils
	sudo apt-get install glmark2
	sudo apt-get install vlc
	sudo apt-get install pinta
	apt-get install intel-opencl-icd
	sudo apt-get install freeglut3-dev
	sudo apt-get install vulkansdk
	sudo apt-get install mesa-vulkan-drivers vulkan-utils

Test Suite Execution :
===================
	Total Test Cases added in the Framework (in Python) : 18
	
	1: 'Check Driver Load',
    2: 'OpenGL - Load Test',
    3: 'Vulkan - Load Test',
    4: 'OpenCV - Load Test',
    5: 'OpenCL - Load Test',
    6: 'Display Resolution Change',
    7: 'Media Playback - VLC',
    8: 'Online Media Streaming.',
    9: 'BaseMark Browser Test for WebGL',
    10: '3D Draw with pinta App',
    11: 'Basic OpenGL Test',
    12: 'G-Flops',
    13: 'Power Management - PM Test',
    14: 'GPU Stress Test Case - (OpenGL)',
    15: 'OpenCV Basic Test',
    16: 'OpenGL Render Test',
    17: 'Vulkan Render Test',
    18: 'OpenCV Functional Test - Camera',
	
	Run the ip_validate.sh file in the Terminal as below:
	
	Single Test :  Parse the Test Number with -t <test_case> argument
		./ip_validate.sh -n gpu -o '-t 1 -i 1'	

	Sanity : Test from 1, 2, 3 ,4, 5 are part of Sanity.
		./ip_validate.sh -n gpu -o '-t sanity'

	Automated : Executes all tests in a single run.
		./ip_validate.sh -n gpu -o '-t automated'

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
		*	gpu		:   IP Validation folder which contains Makefile, main test_gpu.py file, & other binaries. 
		*	logs	:	Contians the exeucted logs files. 
	

Author :
===================
		Ravi Kiran
		Exaleap Semi Confidential. 