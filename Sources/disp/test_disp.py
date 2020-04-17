####################################################################################
# File Name: test_disp.py                                                       								#
# Description: Python test entry file for validating Display                       						#
# Author: Ramesh K P (Divistha Networks)					                                          	#
# Last Modified: 09-March-2020													#
#                                                                               									#
# Copyright: (c) 2019 ExaLeap.                                                  							#
# ExaLeap Proprietary and Confidential. All rights reserved.                    						#
####################################################################################

import sys
import random
import getopt
import os
import subprocess
import time
from fractions import Fraction
import PIL
from PIL import Image
import string
import re
import drawSvg as draw
import webbrowser as wb
import cv2

# Import test specific utilities
sys.path.append('../common')
import testutils

#################################################################################
# Display Constant Definitions                                                     #
#################################################################################

TOTAL_DISP_TESTS            = 14                            # Total number of tests for Display IP

#################################################################################
# Display Global Variables                                                         #
#################################################################################

test_disp_setup_params = {}
test_disp_mode_params = {}

test_disp_test_case_list = {
                             1: 'Validation of Driver Name and Driver Path of Display',
                             2: 'Validation of Resolution, Aspect Ratio, Panel Interface and Frequency',
                             3: 'Change the Resolution and Frequency of the display',
                             4: 'Change the Brightness of the display',
                             5: 'Validation of EDID and DDC information',
                             6: 'Generate different color patterns in the display',
                             7: 'Render 2D vector application',
                             8: 'Validation of color depth',
                             9: 'Validation of loosless image compression and expansion',
                             10: 'Validation of Shading Effect', 
                             11: 'Verification for display configuration in DTS file',
                             12: 'Validation for DMA Monitoring',
                             13: 'Validation for LVDS panel interface',
                             14: 'Validation for different pannels'
                           }

# List of Sanity test cases
test_disp_sanity_list = [ 1 ]
# List of Automated test cases
test_disp_automated_list = [ 2, 7, 8, 10, 11 ]
# List of Manual test cases
test_disp_manual_list = [ 3, 4, 5, 6, 9, 12, 13, 14 ]

#################################################################################
# Display Test Helper Methods                                                      #
#################################################################################

def test_disp_print_usage(prog_name):
    '''Helper method to print the Display test usage'''
    print("Usage: {0} [options]".format(prog_name), flush=True)
    print("  -t <test_case>     Test case group or the integer value representing the test case", flush=True)
    print("                     number. Following test case groups are supported Display:", flush=True)
    print("                       automated:  Run all the test cases in Automated test group.", flush=True)
    print("                       sanity:     Run all the test cases in Sanity test group.", flush=True)
    print("                       manual:     Run all the test cases in Manual test group.", flush=True)
    print("  -h                 Display this information.", flush=True)

def test_disp_get_options(argv):
    '''Helper method to get the Display test parameters'''
    global test_disp_setup_params

    # Initialize the Display test parameters
    test_disp_setup_params['test_case'] = None

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test for Display!'

    try:
        # Get the command line argument lists for the test
        opts, args = getopt.getopt(argv[1:], 't:d:p:s:c:e:h')

        # Iterate the options and get the corresponding values
        for opt, arg in opts:
            if opt  in ('-t'):
                # Test case group or number
                if arg.isdigit():
                    param = int(arg)
                    if param < 1 or param > TOTAL_DISP_TESTS:
                        test_disp_print_usage(argv[0])
                        err_code = testutils.TEST_RESULT_ERROR
                        err_str = 'Invalid test case number ({0}) for the Display testing!'.format(arg)
                        testutils.test_logger.error('%s', err_str)
                        raise testutils.TestFailureException(err_code, err_str)
                    test_disp_setup_params['test_case'] = param
                else:
                    param = arg.lower()
                    if param != 'automated' and param != 'sanity' and param != 'manual':
                        test_disp_print_usage(argv[0])
                        err_code = testutils.TEST_RESULT_ERROR
                        err_str = 'Invalid test case group ({0}) for the Display testing!'.format(arg)
                        testutils.test_logger.error('%s', err_str)
                        raise testutils.TestFailureException(err_code, err_str)
                    test_disp_setup_params['test_case'] = param
            
            elif opt in ('-h'):
                # Usage
                test_disp_print_usage(argv[0])
                err_code = testutils.TEST_RESULT_ERROR
                err_str = 'Not a valid test argument to run the tests!'
                testutils.test_logger.error('%s', err_str)
                raise testutils.TestFailureException(err_code, err_str)

            else:
                # Unknown test option
                test_disp_print_usage(argv[0])
                err_code = testutils.TEST_RESULT_ERROR
                err_str = 'Unrecognized test option ({0}) for the test!'.format(opt)
                testutils.test_logger.error('%s', err_str)
                raise testutils.TestFailureException(err_code, err_str)

        # Test case group or number is mandatory for the testing
        if not bool(test_disp_setup_params['test_case']):
            test_disp_print_usage(argv[0])
            err_code = testutils.TEST_RESULT_ERROR
            err_str = 'Missing test case group or number (option -t) for the testing!'
            testutils.test_logger.error('%s', err_str)
            raise testutils.TestFailureException(err_code, err_str)

        # Current chosen test options
        testutils.test_logger.info('Using below options for the test:')
        if type(test_disp_setup_params['test_case']) == str:
            testutils.test_logger.info('  Test case group:              {0}'.format(test_disp_setup_params['test_case'].capitalize()))
        else:
            testutils.test_logger.info('  Test case number:             {0}'.format(test_disp_setup_params['test_case']))

    except getopt.GetoptError as exc:
        test_disp_print_usage(argv[0])
        if exc.opt == 't' or exc.opt == 'd' or exc.opt == 'p' or exc.opt == 's' or exc.opt == 'c' or exc.opt == 'e':
            err_code = testutils.TEST_RESULT_ERROR
            err_str = 'Missing argument for the test option -{0}!'.format(exc.opt)
            testutils.test_logger.exception('%s', err_str)
        else:
            err_code = testutils.TEST_RESULT_ERROR
            err_str = 'Unrecognized test option character ({0}) for the test!'.format(exc.opt)
            testutils.test_logger.exception('%s', err_str)
        raise testutils.TestFailureException(err_code, err_str)
    except testutils.TestFailureException as exc:
        err_code = exc.err_code
        err_str = exc.err_str
        raise testutils.TestFailureException(err_code, err_str)
    except:
        raise testutils.TestFailureException(err_code, err_str)

def test_disp_execute_case(test_case):
    '''Helper method to execute the requested test case'''
    global test_disp_setup_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    # Initialize the test case result code and message
    testutils.test_case_result_code = testutils.TEST_RESULT_PASS
    testutils.test_case_result_str = None

    # Start the execution of test case
    testutils.test_logger.info('Starting the execution of Display test case %d (%s)', test_case, test_disp_test_case_list[test_case])
    try:
        if test_case == 1:
            test_disp_case_01(test_case)
            #Validation of Driver Name and Driver Path of Display

        elif test_case == 2:
            test_disp_case_02(test_case)
            #Validation of Resolution, Aspect Ratio, Panel Interface and Frequency

        elif test_case == 3:
            test_disp_case_03(test_case)
            #Change the Resolution and Frequency of the display

        elif test_case == 4:
            test_disp_case_04(test_case)
            #Change the Brightness of the display

        elif test_case == 5:
            test_disp_case_05(test_case)
            #Validation of EDID and DDC information

        elif test_case == 6:
            test_disp_case_06(test_case)
            #Generate different color patterns in the display

        elif test_case == 7:
            test_disp_case_07(test_case)
            #Render 2D vector application

        elif test_case == 8:
            test_disp_case_08(test_case)
            #Validation of color depth

        elif test_case == 9:
            test_disp_case_09(test_case)
            #Validation of loosless image compression and expansion

        elif test_case == 10:
            test_disp_case_10(test_case)
            #Validation of Shading Effect

        elif test_case == 11:
            test_disp_case_11(test_case)
            #Verification for display configuration in DTS file    
            
        elif test_case == 12:
            test_disp_case_12(test_case)
            #Validation for DMA Monitoring            
            
        elif test_case == 13:
            test_disp_case_13(test_case)
            #Validation for LVDS panel interface
            
        elif test_case == 14:
            test_disp_case_14(test_case)
            #Validation for different pannels with different timinig

        else:
            # Unknown test case
            err_code = testutils.TEST_RESULT_ERROR
            err_str = 'Unknown test case number ({0}) for the Display testing!'.format(test_case)
            testutils.test_logger.error('%s', err_str)
            raise testutils.TestFailureException(err_code, err_str)

    except testutils.TestFailureException as exc:
        err_code = exc.err_code
        err_str = exc.err_str
    except:
        testutils.test_logger.exception('%s', err_str)
    else:
        err_code = testutils.TEST_RESULT_PASS
        err_str = 'Test case completed without any failures'
        testutils.test_logger.debug('%s', err_str)
    finally:
        # Display test teardown
        try:
            test_disp_teardown()
        except:
            # Ignore any exceptions
            pass

        # Update the test suite result
        testutils.test_suite_update_result(err_code)

        # Update the test report file with test case results
        test_res = testutils.test_get_result_str(err_code)
        file_data = '{0},{1},{2},{3},{4}'.format(test_case, test_disp_test_case_list[test_case], test_res, err_code, err_str)
        testutils.test_write_report_file(file_data)

        # Return immediately for the Fatal failures
        if err_code == testutils.TEST_RESULT_FATAL:
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Setup
#   This function does the initial setup required for the Display, before
#   starting the actual test case.
#
#   Display setup has the following functionalities:
#     1. Configures the ports in the required Display mode.

def test_disp_setup():
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for the method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the Display test setup!'

# Display Test Teardown
#   This function does the final cleanup required for the Display, at the end of
#   the test case (in both successful and failed cases).
#
#   Display teardown has the following functionalities:
#     1. Does any deconfigurations required for the test.

def test_disp_teardown():
    global test_disp_setup_params

    # Initialize the return value for the method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the Display test teardown!'

    try:
        # Display mode parameters
        testutils.test_logger.debug('Cleaning-up the resources used for the Display testing')

    except:
        swpilot_logger.debug('Failed to clean-up the Display test resources!')
        raise testutils.TestFailureException(err_code, err_str)

#################################################################################
# Display test case methods                                                        #
#################################################################################
#   DISPLAY Test Case - 01 (Validation of Driver Name and Driver Path of Display (Load and Unload))
#
#   Test Case Description:
#   Identify the name of the driver used for display in the module and also the path where the driver is present
#
#    Expected Results:
#     1. Display the name of the driver used for display.
#     2. Display the path where the driver is present.

def test_disp_case_01(test_case):
    '''Identify the name of the driver used for display in the module and also the path where the driver is present'''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])

    try:
        # Display test setup
        test_disp_setup()

        disp_driver = os.popen("lspci -nnk | grep -i vga -A3 | grep driver").read()
        if disp_driver:
            #	Shows the name of the display driver used
            disp_driver = disp_driver.split()
            disp_driver = disp_driver[-1]
            testutils.test_logger.debug('The display driver present is : %s', disp_driver)

            #	Shows the path where the display driver is present
            driver_path = os.popen("modinfo {}".format(disp_driver)).read().splitlines()[0].split()
            driver_path = driver_path[-1].strip()
            testutils.test_logger.debug("The path of the display driver is : " + driver_path)

            #	Shows the name of the dependend drivers for display module
            depend_drivers = os.popen("modinfo {} | grep depend".format(disp_driver)).read().split()
            depend_drivers = depend_drivers[1]
            testutils.test_logger.debug("The dependent drivers are : " + depend_drivers)

            err_code = testutils.TEST_RESULT_PASS
            err_str = 'The Driver is present'.format(test_disp_test_case_list[test_case])
            testutils.test_logger.debug('%s', err_str)
            testutils.test_case_update_result(err_code, err_str)   

        else:
            err_code = testutils.TEST_RESULT_FATAL
            err_str = 'Fatal Error for Display during {0}!'.format(test_disp_test_case_list[test_case])
            testutils.test_logger.fatal('%s', err_str)
            testutils.test_logger.fatal('Driver is not present for Display during {}'.format(test_disp_test_case_list[test_case]))
            raise testutils.TestFailureException(err_code, err_str)

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Case - 02 (Validation of Resolution, Aspect Ratio, Panel Interface and Frequency)
#
#   Test Case Description:
#     1. Identifies the Resolution of the display.        
#     2. Identifies the Aspect Ratio of the display.        
#     3. Identifies the Panel Interface of the display.        
#     4. Identifies the Frequency of the display.        
#
#   Expected Results:
#     1. Display the resolution of the display.
#     2. Display the apect ratio of the display.
#     3. Display the panel interface of the display.	
#     4. Display the frequency of the display.

def test_disp_case_02(test_case):
    '''1. Identifies the Resolution of the display.        
      2. Identifies the Aspect Ratio of the display.        
      3. Identifies the Panel Interface of the display.        
      4. Identifies the Frequency of the display.  
    '''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])

    try:
        # Display test setup
        test_disp_setup()

        screen1 = os.popen('xrandr | grep current').read().split('current')[1].strip().split()
        if screen1:
            #	Shows the resolution of the display
            width = screen1[0]
            height = screen1[2][:-1]
            resolution = (width + "x" + height)
            testutils.test_logger.debug("Display Resolution : %s" %(resolution))

            #	Shows the aspect ratio of the display
            ratio = str(Fraction(int(width)/int(height)).limit_denominator()).split('/')
            testutils.test_logger.debug("Display Aspect Ratio : [%s : %s]" %(ratio[0],ratio[1]))

            #	Shows the display panel interface 
            screen2 = os.popen('xrandr | grep {}'.format(resolution)).read().splitlines()
            display_interface = screen2[0].split()[0]
            testutils.test_logger.debug("Display Panel Interface : " + display_interface)

            #	Shows the frequency of the display
            display_frequency = screen2[1].strip().split()[1][:-2]
            testutils.test_logger.debug("Display Frequency : " + display_frequency)

            err_code = testutils.TEST_RESULT_PASS
            err_str = 'Display properties are verified'.format(test_disp_test_case_list[test_case])
            testutils.test_logger.debug('%s', err_str)
            testutils.test_case_update_result(err_code, err_str)   

        else:
            err_code = testutils.TEST_RESULT_FATAL
            err_str = 'Fatal Error for Display during {0}!'.format(test_disp_test_case_list[test_case])
            testutils.test_logger.fatal('%s', err_str)
            testutils.test_logger.fatal('Command is not present for Display during {}'.format(test_disp_test_case_list[test_case]))
            raise testutils.TestFailureException(err_code, err_str)

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Case - 03 (Change the Resolution and Frequency of the display)
#

#   Test Case Description:
#        Change the Resolution of the display (800*)    
#        Change the Frequency of the display
#        Default Resolution is 1920x1080
#        Default Frequency is 60
#
#   Expected Results:
#     Resolution of the display can be changed
#     Frequency of the display can be changed

def test_disp_case_03(test_case):
    '''   Test Case Description:
        Change the Resolution of the display     
        Change the Frequency of the display
    '''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])
 
    try:
        # Display test setup
        test_disp_setup()

        #	Shows the supported display resolution
        screen1 = os.popen('xrandr').read().split('connected')[1].splitlines()
        if screen1:
            supported = screen1[1:-1]
            print("The supported resolutions in current displays are : ")
            for supported in supported:
                print(supported)

            #	Change the resolution of the display
            panel = os.popen("xrandr | grep connected").read().splitlines()[0].split()[0]
            resolution = str(input("Enter the resolution seperated by x : ")).split('x')
            width = resolution[0]
            height = resolution[1]
            res = width + "x" + height
            display = os.popen("xrandr | grep {}".format(res)).read()
            if display:
                os.popen("xrandr -s {}".format(res))
                err_code = testutils.TEST_RESULT_PASS
                err_str = 'Resolution of the Display changed successfully'.format(test_disp_test_case_list[test_case])
                testutils.test_logger.debug('%s', err_str)
                testutils.test_case_update_result(err_code, err_str)   
            else:
                err_code = testutils.TEST_RESULT_ERROR
                err_str = 'Error for Display during {0}!'.format(test_disp_test_case_list[test_case])
                testutils.test_logger.error('%s', err_str)
                testutils.test_logger.error("Entered wrong resolution for Display during {}".format(test_disp_test_case_list[test_case]))
                raise testutils.TestFailureException(err_code, err_str)
 
            #	Change the frequency of the display
            stream = os.popen("xrandr | grep {}".format(res)).read().splitlines()[1].split()
            freq = stream[1:len(stream)]
            print("The supported frequencies for the resolution in current displays are : ")
            frequency = [elem.strip('*+') for elem in freq]
            frequency = [float(i) for i in frequency] 
            frequency = [round(x) for x in frequency]
            res = [] 
            [res.append(x) for x in frequency if x not in res] 
            res = str(res)
            for char in string.punctuation:
                res = res.replace(char, ' ')
            print(res)
            res = res.split()
            freq_change = str(input("Enter the frequency : "))
            if freq_change == res[0] or freq_change == res[1]:
                os.popen("xrandr -r {}".format(freq_change))
                err_code = testutils.TEST_RESULT_PASS
                err_str = 'Frequency of the Display changed successfully'.format(test_disp_test_case_list[test_case])
                testutils.test_logger.debug('%s', err_str)
                testutils.test_case_update_result(err_code, err_str)   

            else:
                err_code = testutils.TEST_RESULT_ERROR
                err_str = 'Error for Display during {0}!'.format(test_disp_test_case_list[test_case])
                testutils.test_logger.error('%s', err_str)
                testutils.test_logger.error("Entered wrong frequency for Display during {}".format(test_disp_test_case_list[test_case]))
                raise testutils.TestFailureException(err_code, err_str)
        else:
            err_code = testutils.TEST_RESULT_FATAL
            err_str = 'Fatal Error for Display during {0}!'.format(test_disp_test_case_list[test_case])
            testutils.test_logger.fatal('%s', err_str)
            testutils.test_logger.fatal('Command is not present for Display during {}'.format(test_disp_test_case_list[test_case]))
            raise testutils.TestFailureException(err_code, err_str)

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Case - 04 (Change the brightness level of the Display)
#
#   Test Case Description:
#     Change different brightness level of the display.
#
#   Expected Results:
#     Changed different brightness level of the display.

def test_disp_case_04(test_case):
    '''Change different brightness level of the display.'''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])

    try:
        # Display test setup
        test_disp_setup()
        
        #	Check the display panel
        panel = os.popen("xrandr | grep connected").read().splitlines()[0].split()[0]
        if panel:
            #	Change the brightness of the screen
            bright = input("Enter the Brightness level (10 - 100) : ")
            bright = int(bright)/100
            if bright > 0.1 and bright <=1:
                os.popen("xrandr --output {} --brightness {}".format(panel, bright))
                err_code = testutils.TEST_RESULT_PASS
                err_str = 'Changed the brightness level of the display successfully'.format(test_disp_test_case_list[test_case])
                testutils.test_logger.debug('%s', err_str)
                testutils.test_case_update_result(err_code, err_str)   
            else:
                err_code = testutils.TEST_RESULT_ERROR
                err_str = 'Error for Display during {0}!'.format(test_disp_test_case_list[test_case])
                testutils.test_logger.error('%s', err_str)
                testutils.test_logger.fatal('Entered wrong brightness level for Display during {}'.format(test_disp_test_case_list[test_case]))
                raise testutils.TestFailureException(err_code, err_str)
        else:
            err_code = testutils.TEST_RESULT_FATAL
            err_str = 'Fatal Error for Display during {0}!'.format(test_disp_test_case_list[test_case])
            testutils.test_logger.fatal('%s', err_str)
            testutils.test_logger.fatal('Command is not present for Display during {}'.format(test_disp_test_case_list[test_case]))
            raise testutils.TestFailureException(err_code, err_str)

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Case - 05 (Validation of EDID and DDC information)
#
#   Test Case Description:
#     Shows the EDID (Extended Display Identification Data) and DDC (Display Data Channel) information
#
#   Expected Results:
#     EDID and DDC information of the display are displayed

def test_disp_case_05(test_case):
    '''Shows the EDID (Extended Display Identification Data) and DDC (Display Data Channel) information'''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])

    try:
        # Display test setup
        test_disp_setup()

        #	Check the EDID information
        os.popen("sudo get-edid > a.txt").read()
        time.sleep(2)        
        try:
            edid = os.popen("sudo parse-edid < a.txt").read()
            if edid:
                edid_info = os.popen("sudo parse-edid < a.txt | grep -i identifier -A2").read()
                #	Shows the Identifiers name of the display
                identifier = edid_info.splitlines()[0].split('"')[1]
                testutils.test_logger.debug("The identifier name is : " + identifier)
                #	Shows the Model name of the display
                model = edid_info.splitlines()[1].split('"')[1]
                testutils.test_logger.debug("The Model name is : " + model)	
                #	Shows the Vendor name of the display
                vendor = edid_info.splitlines()[2].split('"')[1]
                testutils.test_logger.debug("The Vendor name is : " + vendor)

        except:
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            err_code = testutils.TEST_RESULT_CRITICAL
            err_str = 'Critical Error for Display during {0}!'.format(test_disp_test_case_list[test_case])
            testutils.test_logger.critical('%s', err_str)
            testutils.test_logger.fatal('Hardware is not connected properly for Display during {}'.format(test_disp_test_case_list[test_case]))
            raise testutils.TestFailureException(err_code, err_str)

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Case - 06 (Generate different color patterns in the display)
#
#   Test Case Description:
#     Generat different color patterns in the display.
#
#   Expected Results:
#     Different color images are generated and diaplayed in the display module

def test_disp_case_06(test_case):
    '''Generat different color patterns in the display.'''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])

    try:
        # Display test setup
        test_disp_setup()

        image = input("Enter the color to generate : ")

        #	Generates the color pattern according to the input given
        '''
        aliceblue, antiquewhite, aqua, aquamarine, azure, 
        beige, bisque, black, blanchedalmond, blue, blueviolet, brown, burlywood, 
        cadetblue, chartreuse, chocolate, coral, cornflowerblue, cornsilk, crimson, cyan, 
        darkblue, darkcyan, darkgoldenrod, darkgray, darkgreen, darkkhaki, darkmagenta, darkolivegreen, darkorange, darkorchid, darkred, darksalmon, darkseagreen, darkslateblue, darkslategray, 
        darkslategrey, darkturquoise, darkviolet, deeppink, deepskyblue, dimgray, dimgrey, dodgerblue, 
        firebrick, floralwhite, forestgreen, fuchsia, 
        gainsboro, ghostwhite, gold, goldenrod, gray, grey, green, greenyellow, 
        honeydew, hotpink, 
        indianred, indigo, ivory, 
        khaki, 
        lavender, lavenderblush, lawngreen, lemonchiffon, lightblue, lightcoral, lightcyan, lightgoldenrodyellow, lightgreen, lightgray, lightgrey, lightpink, lightsalmon, lightseagreen, lightskyblue, 
        lightslategray, lightslategrey, lightsteelblue, lightyellow, lime, limegreen, linen, 
        magenta, maroon, mediumaquamarine, mediumblue, mediumorchid, mediumpurple, mediumseagreen, mediumslateblue, mediumspringgreen, mediumturquoise, mediumvioletred, midnightblue, 
        mintcream, mistyrose, moccasin, 
        navajowhite, navy, 
        oldlace, olive, olivedrab, orange, orangered, orchid, 
        palegoldenrod, palegreen, paleturquoise, palevioletred, papayawhip, peachpuff, peru, pink, plum, powderblue, purple, 
        rebeccapurple, red, rosybrown, royalblue,
        saddlebrown, salmon, sandybrown, seagreen, seashell, sienna, silver, skyblue, slateblue, slategray, slategrey, snow, springgreen, steelblue, 
        tan, teal, thistle, tomato, turquoise, 
        violet, 
        wheat, white, whitesmoke, 
        yellow, yellowgreen,
        '''
        img = Image.new('RGB', (960, 540), color = '{}'.format(image))
        img = img.save('{}.jpg'.format(image))
        img = cv2.imread('{}.jpg'.format(image))
        cv2.imshow('{}.jpg'.format(image), img)
        cv2.waitKey(0)  
        cv2.destroyAllWindows() 
        os.remove('{}.jpg'.format(image)) 

        err_code = testutils.TEST_RESULT_PASS
        err_str = 'Different color patterns are generated in the Display module'.format(test_disp_test_case_list[test_case])
        testutils.test_logger.debug('%s', err_str)
        testutils.test_case_update_result(err_code, err_str)   

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Case - 07 (Render 2D vector application)
#
#   Test Case Description:
#     Generates 2D vector images in the screen.
#
#   Expected Results:
#     Vector images are generated

def test_disp_case_07(test_case):
    '''Generates 2D vector images in the screen.'''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])

    try:
        # Display test setup
        test_disp_setup()
        
        #	Generates 2D vector images
        d = draw.Drawing(1200, 600, origin='center')
        d.append(draw.Lines(-500, 50, -200, 50, -200, 250, -500, 250, -500, 50, stroke_width=5, fill='#eeee00', stroke='black'))
        d.append(draw.Rectangle(200,50,300,200, fill='#1248ff', stroke_width=5, stroke='red'))
        d.append(draw.Circle(0, -50, 50, fill='red', stroke_width=5, stroke='black'))

        p = draw.Path(stroke_width=5, stroke='green', fill='black', fill_opacity=1)
        p.M(250,100)
        p.l(200,0)
        p.v(100)
        p.h(-200)
        p.Z()
        d.append(p)
        d.saveSvg('2.svg')
        wb.open("2.svg")

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Case - 08 (Validation of color depth)
#
#   Test Case Description:
#     Identify the different color depths supported by the display
#     Identify the current color depth of the display
#
#   Expected Results:
#     Identified the different color depths supported by the display and also the current color depth of the display

def test_disp_case_08(test_case):
    '''Identify the different color depths supported by the display
      Identify the current color depth of the display'''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])

    try:
        # Display test setup
        test_disp_setup()
        
        supported = os.popen('xdpyinfo | grep depths').read().split(':')[1].strip()
        if supported:
            testutils.test_logger.debug("The Supported Color Depths are : " + supported)
        else:
            err_code = testutils.TEST_RESULT_ERROR
            err_str = 'Fatal Error for Display during {0}!'.format(test_disp_test_case_list[test_case])
            testutils.test_logger.fatal('%s', err_str)
            testutils.test_logger.fatal('Command is not present for Display during {}'.format(test_disp_test_case_list[test_case]))
            raise testutils.TestFailureException(err_code, err_str)

        #	Current color depth of the Display
        current = os.popen('xwininfo -root | grep Depth').read().split()
        if current:
            testutils.test_logger.debug("The Current Color Depth of the Display is : " + current[1])
        else:
            err_code = testutils.TEST_RESULT_ERROR
            err_str = 'Fatal Error for Display during {0}!'.format(test_disp_test_case_list[test_case])
            testutils.test_logger.fatal('%s', err_str)
            testutils.test_logger.fatal('Command is not present for Display during {}'.format(test_disp_test_case_list[test_case]))
            raise testutils.TestFailureException(err_code, err_str)

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Case - 09 (Validation of loosless image compression and expansion)
#
#   Test Case Description:
#     Validation of loosless image compression and expansion
#
#   Expected Results:
#     Generated loosless image after compression and expansion

def test_disp_case_09(test_case):
    '''Generated loosless image after compression and expansion'''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])

    try:
        # Display test setup
        test_disp_setup()
        
        img_lst = ['alto', 'car', 'check', 'hummer', 'lake', 'sea']
        print("The available images are : ")
        print("1.	alto")
        print("2.	car")
        print("3.	check")
        print("4.	hummer")
        print("5.	lake")
        print("6.	sea")

        picture = input("Enter name of the picture : ")
        if picture in str(img_lst):
            #	shows the original pixel size of the image
            image = cv2.imread('{}.jpg'.format(picture))
            h,w,c = image.shape
            original_pixel = w * h
            print("Original width : " + str(w))
            print("Original height : " + str(h))
            print("Pixel size of original image is : " + str(original_pixel))

            #	enter the length and height to create the new image
            length = int(input("Enter the width of the picture : "))
            height = int(input("Enter the height of the picture : "))
            entered = length * height
            testutils.test_logger.debug("Pixel sixe of enterd values is : " + str(entered))

            #	shows the pixel size of the new image formed
            img = Image.open('{}.jpg'.format(picture))
            img = img.resize((length, height), PIL.Image.ANTIALIAS)
            img.save('resized_{}.jpg'.format(picture))
            new_img = cv2.imread('resized_{}.jpg'.format(picture))
            time.sleep( 5 )
            nh,nw,nc = new_img.shape
            new_pixel = nw*nh
            testutils.test_logger.debug("New width : " + str(nw))
            testutils.test_logger.debug("New height : " + str(nh))
            testutils.test_logger.debug("Pixel size of new image is : " + str(new_pixel))

            cv2.imshow('original', image) 
            cv2.imshow('new', new_img) 
            cv2.waitKey(0)  
            cv2.destroyAllWindows() 
            os.remove('resized_{}.jpg'.format(picture))

        else:
            err_code = testutils.TEST_RESULT_ERROR
            err_str = 'Error for Display during {0}!'.format(test_disp_test_case_list[test_case])
            testutils.test_logger.error('%s', err_str)
            testutils.test_logger.fatal('Entered wrong name of image for Display during {}'.format(test_disp_test_case_list[test_case]))
            raise testutils.TestFailureException(err_code, err_str)

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Case - 10 (Validation of Shading Effect)
#
#   Test Case Description:
#     Image transparency using alpha blending
#
#   Expected Results:
#     Image transparency is done using alpha blending

def test_disp_case_10(test_case):
    '''Image transparency using alpha blending.'''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])

    try:
        # Display test setup
        test_disp_setup()
        
        # function to overlay a transparent image on backround.
        def transparentOverlay(src , overlay , pos=(0,0),scale = 1):
            """
            :param src: Input Color Background Image
            :param overlay: transparent Image (BGRA)
            :param pos:  position where the image to be blit.
            :param scale : scale factor of transparent image.
            :return: Resultant Image 
            """
            overlay = cv2.resize(overlay,(0,0),fx=scale,fy=scale)
            """
            cv2.resize(overlay, dsize, fx, fy)
            :param overlay: Input Color Foreground Image	
            :param dsize: Desired Size for the Output Image
            :param fx: Scale Factor Along the Horizontal Axis
            :param fy: Scale Factor Along the Vertical Axis
            """
            #	Height, Width and Channels of Input Color Foreground Image	
            h,w,c = overlay.shape
            #	Height, Width and Channels of Input Color Background Image	
            rows,cols,chnls = src.shape
    
            y,x = pos[0],pos[1]    # Position of PngImage
        
            #	loop over all pixels and apply the blending equation
            for i in range(h):
                for j in range(w):
                    if x+i >= rows or y+j >= cols:
                        continue
                    alpha = float(overlay[i][j][3]/255.0) # read the alpha channel 
                    src[x+i][y+j] = alpha*overlay[i][j][:3]+(1-alpha)*src[x+i][y+j]
            return src

        """ ----------- Read all images --------------------"""
        bImg = cv2.imread("background.jpg")

        #	KeyPoint : Remember to use cv2.IMREAD_UNCHANGED flag to load the image with alpha channel
        pngImage = cv2.imread("foreground.png" , cv2.IMREAD_UNCHANGED)
        logoImage = cv2.imread("logo.png",cv2.IMREAD_UNCHANGED)

        #	Overlay transparent images at desired postion(x,y) and Scale. 
        result = transparentOverlay(bImg,pngImage,(300,0),0.7)
        result = transparentOverlay(bImg,logoImage,(800,400),2)

        #	Display the result 
        cv2.namedWindow("Result",cv2.WINDOW_NORMAL)
        cv2.imshow("Result" ,result)
        cv2.waitKey()
        cv2.destroyAllWindows()

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Case - 11 (Verification for display configuration in DTS file)
#
#   Test Case Description:
#     Verify the display configuration in DTS file
#
#   Expected Results:
#     Verified the display configuration in DTS file

def test_disp_case_11(test_case):
    '''Verify the display configuration in DTS file'''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])

    try:
        # Display test setup
        test_disp_setup()

        err_code = testutils.TEST_RESULT_SKIP
        err_str = 'Skip the test case for Display during {0}!'.format(test_disp_test_case_list[test_case])
        testutils.test_logger.skip('%s', err_str)
        testutils.test_logger.skip('Hardware is not present for Display during {}'.format(test_disp_test_case_list[test_case]))
        raise testutils.TestFailureException(err_code, err_str)

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Case - 12 (Validation for DMA Monitoring)
#
#   Test Case Description:
#     Validation the DMA monitoring in the system
#
#   Expected Results:
#     Validates the DMA monitoring in the system

def test_disp_case_12(test_case):
    '''Validation the DMA monitoring in the system'''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])

    try:
        # Display test setup
        test_disp_setup()

        err_code = testutils.TEST_RESULT_SKIP
        err_str = 'Skip the test case for Display during {0}!'.format(test_disp_test_case_list[test_case])
        testutils.test_logger.skip('%s', err_str)
        testutils.test_logger.skip('Hardware is not present for Display during {}'.format(test_disp_test_case_list[test_case]))
        raise testutils.TestFailureException(err_code, err_str)

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Case - 13 (Validation for LVDS panel interface)
#
#   Test Case Description:
#     Validation of LVDS panel
#
#   Expected Results:
#     Validates the LVDS panel

def test_disp_case_13(test_case):
    ''' Validation of LVDS panel'''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])

    try:
        # Display test setup
        test_disp_setup()

        err_code = testutils.TEST_RESULT_SKIP
        err_str = 'Skip the test case for Display during {0}!'.format(test_disp_test_case_list[test_case])
        testutils.test_logger.skip('%s', err_str)
        testutils.test_logger.skip('Hardware is not present for Display during {}'.format(test_disp_test_case_list[test_case]))
        raise testutils.TestFailureException(err_code, err_str)

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

# Display Test Case - 14 (Validation for different pannels with different timinig)
#
#   Test Case Description:
#     Validation for different pannels with different timinig
#
#   Expected Results:
#     Validates different pannels with different timinig

def test_disp_case_14(test_case):
    '''Validation for different pannels with different timinig'''
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!'.format(test_case, test_disp_test_case_list[test_case])

    testutils.test_logger.debug('TestCase-%02d: Testing Display %s with following parameters:', test_case, test_disp_test_case_list[test_case])

    try:
        # Display test setup
        test_disp_setup()

        err_code = testutils.TEST_RESULT_SKIP
        err_str = 'Skip the test case for Display during {0}!'.format(test_disp_test_case_list[test_case])
        testutils.test_logger.skip('%s', err_str)
        testutils.test_logger.skip('Hardware is not present for Display during {}'.format(test_disp_test_case_list[test_case]))
        raise testutils.TestFailureException(err_code, err_str)

    except:
        testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
        raise

    finally:
        # Check for any error without exceptions
        if testutils.test_case_result_code:
            err_code = testutils.test_case_result_code
            err_str = testutils.test_case_result_str
            testutils.test_logger.debug('Failed for Display %s', test_disp_test_case_list[test_case])
            raise testutils.TestFailureException(err_code, err_str)

#################################################################################
# Main entry point for the Display test                                            #
#################################################################################

def test_disp_main(argv):
    global test_disp_setup_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test suite for Display!'

    # Start the Display IP validation
    test_msg = 'Display IP validation'
    try:
        # Initialize the random number generator
        if not testutils.test_random_seed:
            testutils.test_random_seed = int(time.time())
        testutils.test_logger.debug('Using the random seed of %d for the Python tests', testutils.test_random_seed)
        random.seed(testutils.test_random_seed)

        # Parse the command line arguments
        test_disp_get_options(argv)

        # Total number of test cases
        if type(test_disp_setup_params['test_case']) == str:
            # Test group with multiple test cases
            test_disp_cases_group = True
            if test_disp_setup_params['test_case'] == 'automated':
                test_disp_cases_total = len(test_disp_automated_list)
            elif test_disp_setup_params['test_case'] == 'sanity':
                test_disp_cases_total = len(test_disp_sanity_list)
            elif test_disp_setup_params['test_case'] == 'manual':
                test_disp_cases_total = len(test_disp_manual_list)
            else:
                err_code = testutils.TEST_RESULT_ERROR
                err_str = 'Invalid test case group ({0}) for the Display testing!'.format(test_disp_setup_params['test_case'])
                testutils.test_logger.error('%s', err_str)
                raise testutils.TestFailureException(err_code, err_str)
        else:
            # Individual test cases
            test_disp_cases_group = False
            test_disp_cases_total = 1

        # Start the Display test suite
        if test_disp_cases_group:
            test_msg = '{0} with {1} suite of {2} test case(s)'.format(test_msg, test_disp_setup_params['test_case'].capitalize(), test_disp_cases_total)
        else:
            test_msg = '{0} with Single test case'.format(test_msg)
        testutils.test_logger.info('Starting the {0}'.format(test_msg))

        # Check the test report file accessibility
        file_data = ':: Test report for {0} ::'.format(test_msg)
        testutils.test_check_report_file_access(file_data)

        # Write the test report header
        file_data = 'Test_Case_Number,Test_Case_Desc,Test_Result,Test_Err_Code,Test_Result_Desc'
        testutils.test_write_report_file(file_data)

        # Loop through the test cases for Display
        for test_index in range(test_disp_cases_total):
            if test_disp_cases_group:
                if test_disp_setup_params['test_case'] == 'automated':
                    test_case = test_disp_automated_list[test_index]
                elif test_disp_setup_params['test_case'] == 'sanity':
                    test_case = test_disp_sanity_list[test_index]
                elif test_disp_setup_params['test_case'] == 'manual':
                    test_case = test_disp_manual_list[test_index]
            else:
                test_case = test_disp_setup_params['test_case']

            # Start the execution of test case
            test_disp_execute_case(test_case)

    except testutils.TestFailureException as exc:
        err_code = exc.err_code
        err_str = exc.err_str
        # Update the test suite result
        testutils.test_suite_update_result(err_code)
    except:
        testutils.test_logger.exception('%s', err_str)
        # Update the test suite result
        testutils.test_suite_update_result(err_code)
    else:
        err_code = testutils.TEST_RESULT_PASS
        err_str = 'Successfully completed the {0}'.format(test_msg)
        testutils.test_logger.debug('%s', err_str)
    finally:
        # Return with the test results
        res_str = testutils.test_get_result_str(testutils.test_suite_result_code)
        if testutils.test_suite_result_code:
            testutils.test_logger.info('One or more failures observed for %s with return code %d (%s)!', test_msg, testutils.test_suite_result_code, res_str)
        else:
            testutils.test_logger.info('%s completed successfully with return code %d (%s)', test_msg, testutils.test_suite_result_code, res_str)
        return testutils.test_suite_result_code

if __name__ == '__main__':
    status = test_disp_main(sys.argv)
    sys.exit(status)



