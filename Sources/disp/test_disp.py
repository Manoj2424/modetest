#!/usr/bin/python

#################################################################################
# File Name: test_gpu.py                                                        #
# Description: Python test entry file for validating DISPLAY                    #
# Author: Ganesh Shanubhogue (DevSys)                                           #
# Last Modified: 10-Feb-2020                                                    #
#                                                                               #
# Copyright: (c) 2019 ExaLeap.                                                  #
# ExaLeap Proprietary and Confidential. All rights reserved.                    #
#################################################################################
import sys
import random
import getopt
import os
import subprocess
import time
import logging
import signal
import cv2
import numpy as np


# Import test specific utilities
sys.path.append('../common')
import testutils

# import validator

#################################################################################
# DISPLAY Constant Definitions                                                     #
#################################################################################
TOTAL_DISPLAY_TESTS = 20  # Total number of tests for DISPLAY IP
DISP_TEST_C_BINARY_FILE = './bin/test_disp'  # DISPLAY test binary file for executing test cases implemented in C
# TEST_DISPLAY_SUPP_BAUD_RATE    = [9600, 19200, 38400, 57600, 115200]
# TEST_DISPLAY_SUPP_DATA_BITS    = [5, 6, 7, 8]
# TEST_DISPLAY_SUPP_PARITY_BITS  = ['none', 'even', 'odd', 'mark', 'space']
# TEST_DISPLAY_SUPP_STOP_BITS    = ['1p0', '1p5', '2p0']

#################################################################################
# DISPLAY Global Variables                                                         #
#################################################################################
test_disp_setup_params = {}
test_disp_mode_params = {}
iteration = 1
# List of supported test cases for DISPLAY
test_disp_test_case_list = {
    1: 'NB2_DISP_01 : Check fb0 Support.',
    2: 'NB2_DISP_02 : Display Interface and Resolution Info',
    3: 'NB2_DISP_03 : Render a Image/Program on Display',
    4: 'NB2_DISP_04 : Generate Color Palette from a Image.',
    5: 'NB2_DISP_05 : Change Brightness',
    6: 'NB2_DISP_06 : Alpha Blending',
    7: 'NB2_DISP_07 : Image Scaling',
    8: 'NB2_DISP_08 : Display EDID Info',
    9: 'NB2_DISP_09 : Change Display Resolution',
    10: 'NB2_DISP_10 : Change Color Depth',
    11: 'NB2_DISP_11 : Depth & Pixel Info from Image',
    12: 'NB2_DISP_12 : Change Image Color Bit',
    13: 'NB2_DISP_13 : Create and Render a Image',
    14: 'NB2_DISP_14 : OverLay Support'
}
# List of Automated test cases
test_disp_automated_list = [1, 2, 3, 4, 6, 7, 11, 12, 13, 14]
# List of Sanity test cases
test_disp_sanity_list = [1, 2, 3]
# List of Manual test cases
test_disp_manual_list = [3, 8, 9]


#################################################################################
# DISPLAY Test Helper Methods                                                      #
#################################################################################
# Helper method to print the DISPLAY test usage
def test_disp_print_usage(prog_name):
    print("", flush=True)
    print("Usage: {0} [options]".format(prog_name), flush=True)
    print("  -t <test_approach>     Test case group or the integer value representing the test case", flush=True)
    print("                         number. Following test case groups are supported DISPLAY:", flush=True)
    print("                             automated:  Run all the test cases in Automated test group.", flush=True)
    print("                             sanity:     Run all the test cases in Sanity test group.", flush=True)
    print("                             manual:     Run all the test cases in Manual test group.", flush=True)
    print("  -t <test_number>           NB2_DISP_01. Check fb0 Support ", flush=True)
    print("                             NB2_DISP_02. Display Interface and Resolution Info", flush=True)
    print("                             NB2_DISP_03. Render a Image/Program on Display", flush=True)
    print("                             NB2_DISP_04. Generate Color Palette from a Image.", flush=True)
    print("                             NB2_DISP_05. Change Brightness", flush=True)
    print("                             NB2_DISP_06. Alpha Blending", flush=True)
    print("                             NB2_DISP_07. Image Scaling", flush=True)
    print("                             NB2_DISP_08. Display EDID Info", flush=True)
    print("                             NB2_DISP_09. Change Display Resolution", flush=True)
    print("                             NB2_DISP_10. Change Color Depth.", flush=True)
    print("                             NB2_DISP_11. Depth & Pixel Info from Image", flush=True)
    print("                             NB2_DISP_12. Change Image Color Depth ", flush=True)
    print("                             NB2_DISP_13. Create and Render a Image", flush=True)
    print("                             NB2_DISP_14. OverLay Support", flush=True)
    print("  -i <iteration>         Allows test Case to execute over a certain Iterations. ", flush=True)
    print("                             -i <iteration_count> where '-i' accepts integer value.", flush=True)
    print("                             -i 10   -> Where test executes 10 iteration.", flush=True)
    print("  -h                     Shows help page with all the available options.", flush=True)
    print("", flush=True)


# Helper method to get the DISPLAY test parameters
def test_disp_get_options(argv):
    global test_disp_setup_params
    global iteration

    # Initialize the DISPLAY test parameters
    test_disp_setup_params['test_case'] = None
    # test_disp_setup_params['pri_dev'] = ''
    # test_disp_setup_params['sec_dev'] = ''
    # test_disp_setup_params['setup_type'] = 'single'
    # test_disp_setup_params['ext_dev_type'] = 'host'

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test for Display!'

    try:
        # Get the command line argument lists for the test
        opts, args = getopt.getopt(argv[1:], 't:i:h')

        # Iterate the options and get the corresponding values
        for opt, arg in opts:
            if opt in ('-t'):
                # Test case group or number
                if arg.isdigit():
                    param = int(arg)
                    if param < 1 or param > TOTAL_DISPLAY_TESTS:
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
            # Looking for -i option for run test in iterations.
            elif opt in ('-i'):
                if arg.isdigit():
                    iteration = int(arg)
                    if iteration > 0:
                        testutils.test_logger.info("{0} Iteration is now Set for : {1} ".format(time.asctime(),
                                                                                                iteration))
                    elif iteration <= 0:
                        iteration = 1
                        testutils.test_logger.info("{0} Setting Iteration to default : 1".format(time.asctime()))
                else:
                    testutils.test_logger.error("{0}    Invalid Iteration type, Enter integer's only."
                                                .format(time.asctime()))
                    err_code = testutils.TEST_RESULT_ERROR
                    err_str = "Invalid Iteration type, Enter integer's only."
                    raise testutils.TestFailureException(err_code, err_str)
            # Setting up for help to display all the available profiles..
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

        if not bool(test_disp_setup_params['test_case']):
            test_disp_print_usage(argv[0])
            err_code = testutils.TEST_RESULT_ERROR
            err_str = 'Missing test case group or number (option -t) for the testing!'
            testutils.test_logger.error('%s', err_str)
            raise testutils.TestFailureException(err_code, err_str)

    except getopt.GetoptError as exc:
        test_disp_print_usage(argv[0])
        if exc.opt == 't' or exc.opt == 'i':
            err_code = testutils.TEST_RESULT_ERROR
            err_str = 'Missing argument for the test option -{0}!'.format(exc.opt)
            raise testutils.TestFailureException(err_code, err_str)
        else:
            err_code = testutils.TEST_RESULT_ERROR
            err_str = 'Invalid argument for the test option -{0}!'.format(exc.opt)
            raise testutils.TestFailureException(err_code, err_str)


# Helper method to execute the requested test case
def test_disp_execute_case(test_case):
    global test_disp_setup_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test case {0} ({1}) for Display!' \
        .format(test_case, test_disp_test_case_list[test_case])

    # Initialize the test case result code and message
    testutils.test_case_result_code = testutils.TEST_RESULT_PASS
    testutils.test_case_result_str = None

    # Command to run the C test binary
    test_cmd = '{0} -t {1}'.format(DISP_TEST_C_BINARY_FILE, test_case)

    # Start the execution of test case
    testutils.test_logger.info('Starting the execution of Display test case %d (%s)', test_case,
                               test_disp_test_case_list[test_case])
    try:
        # Execute the test case
        if test_case == 1:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_01 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                fb0_enabled()
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 2:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_02 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                get_display_info()
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 3:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_03 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                render_program_display()

        elif test_case == 4:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_04 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                color_palette()

        elif test_case == 5:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_05 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                change_brightness()

        elif test_case == 6:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_06 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                alpha_blending()

        elif test_case == 7:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_07 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                img_scaling()

        elif test_case == 8:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_08 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                get_edid()

        elif test_case == 9:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_09 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                change_resolution()

        elif test_case == 10:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_10 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                depth_change()

        elif test_case == 11:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_11 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                get_img_info()

        elif test_case == 12:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_12 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                change_color_depth()

        elif test_case == 13:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_13 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                render_image()

        elif test_case == 14:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: DISP_14 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                overlay_support()

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
        # DISPLAY test teardown
        try:
            test_disp_teardown()
        except:
            # Ignore any exceptions
            pass

        # Update the test suite result
        testutils.test_suite_update_result(err_code)

        # Update the test report file with test case results
        test_res = testutils.test_get_result_str(err_code)
        file_data = '{0},{1},{2},{3},{4}'.format(test_case, test_disp_test_case_list[test_case], test_res, err_code,
                                                 err_str)
        testutils.test_write_report_file(file_data)

        # Return immediately for the Fatal failures
        if err_code == testutils.TEST_RESULT_FATAL:
            raise testutils.TestFailureException(err_code, err_str)


# DISPLAY Test Setup
#   This function does the initial setup required for the DISPLAY, before
#   starting the actual test case.
#
#   DISPLAY setup has the following functionality:
#     1. Configures the ports in the required DISPLAY mode.


def test_disp_setup():
    global test_disp_setup_params
    global test_disp_mode_params

    # Initialize the return value for the method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the DISPLAY test setup!'

    try:
        # DISPLAY mode parameters
        baud_rate = test_disp_mode_params['baud_rate']
        data_bit_len = test_disp_mode_params['data_bit_len']
        parity = test_disp_mode_params['parity']
        stop_bits = test_disp_mode_params['stop_bits']
        testutils.test_logger.debug('Setting up Display with following configurations:')
        testutils.test_logger.debug('  Baud rate:       %d', baud_rate)
        testutils.test_logger.debug('  Data bit length: %d', data_bit_len)
        testutils.test_logger.debug('  Parity:          %s', parity.capitalize())
        testutils.test_logger.debug('  Stop bits:       %s', stop_bits.upper())

    except:
        swpilot_logger.debug('Failed to setup DISPLAY for the requested mode!')
        raise testutils.TestFailureException(err_code, err_str)


# DISPLAY Test Teardown
#   This function does the final cleanup required for the DISPLAY, at the end of
#   the test case (in both successful and failed cases).
#
#   DISPLAY teardown has the following functionalities:
#     1. Does any deconfigurations required for the test.
def test_disp_teardown():
    global test_disp_setup_params

    # Initialize the return value for the method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the DISPLAY test teardown!'

    try:
        # DISPLAY mode parameters
        testutils.test_logger.debug('Cleaning-up the resources used for the Display testing')

    except:
        swpilot_logger.debug('Failed to clean-up the DISPLAY test resources!')
        raise testutils.TestFailureException(err_code, err_str)


#################################################################################
# Main entry point for the DISPLAY test                                            #
#################################################################################
def test_disp_main(argv):
    global test_disp_setup_params

    # Initialize the return value for method
    err_code = testutils.TEST_RESULT_ERROR
    err_str = 'Unknown Python program failure while executing the test suite for Display!'

    # Start the Display IP validation
    test_msg = 'Display - IP validation'
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
                err_str = 'Invalid test case group ({0}) for the Display testing!'.format(
                    test_disp_setup_params['test_case'])
                testutils.test_logger.error('%s', err_str)
                raise testutils.TestFailureException(err_code, err_str)
        else:
            # Individual test cases
            test_disp_cases_group = False
            test_disp_cases_total = 1

        # Start the DISPLAY test suite
        if test_disp_cases_group:
            test_msg = '{0} with {1} suite of {2} test case(s)'.format(test_msg,
                                                                       test_disp_setup_params['test_case'].capitalize(),
                                                                       test_disp_cases_total)
        else:
            test_msg = '{0} with Single test case'.format(test_msg)
        testutils.test_logger.info('Starting the {0}'.format(test_msg))

        # Check the test report file accessibility
        file_data = ':: Test report for {0} ::'.format(test_msg)
        testutils.test_check_report_file_access(file_data)

        # Write the test report header
        file_data = 'Test_Case_Number,Test_Case_Desc,Test_Result,Test_Err_Code,Test_Result_Desc'
        testutils.test_write_report_file(file_data)

        # Loop through the test cases for DISPLAY
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
            testutils.test_logger.info('One or more failures observed for %s with return code %d (%s)!',
                                       test_msg, testutils.test_suite_result_code, res_str)
        else:
            testutils.test_logger.info('%s completed successfully with return code %d (%s)', test_msg,
                                       testutils.test_suite_result_code, res_str)
        return testutils.test_suite_result_code


# # #
#
#   01. Check fb0 enabled..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#
# # #

def fb0_enabled():
    path = "/dev/fb0"
    testutils.test_logger.info("{0} : Checking fbo status.." .format(time.asctime()))
    if os.path.exists(path):
        testutils.test_logger.info("{0} : fb0 found in path (/dev/fb0) in the System." .format(time.asctime()))
        err_code = testutils.TEST_RESULT_PASS
        err_str = "{0} : fb0 Character file available.." .format(time.asctime())
        testutils.test_case_update_result(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : fb0 not available." .format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. " .format(time.asctime())
        testutils.test_logger.fatal(err_code, err_str)
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   02. Check External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   Prints the -> Display Resolution,
#              -> Display Supported Interfaces, and their status.
#
# # #

def get_display_info():
    io_cmd = r'for p in /sys/class/drm/*/status; do con=${p%/status}; echo -n "${con#*/card?-}: "; cat $p; done'
    mod_cmd = r'for i in $(ls -1 /sys/class/drm/*/modes); do echo "$i:"; cat $i; done'
    testutils.test_logger.info("{0} : Trying to fetch, Display interfaces and Info..." .format(time.asctime()))
    f_path = "/dev/fb0"
    testutils.test_logger.info("{0} : Checking fbo status..".format(time.asctime()))
    if os.path.exists(f_path):
        testutils.test_logger.info("{0} : fb0 found in path (/dev/fb0) in the System.".format(time.asctime()))
        testutils.test_logger.info("{0} : Checking for Display configs.." .format(time.asctime()))
        fb_info = subprocess.check_output("sudo fbset", shell=True)
        io_info = subprocess.check_output(io_cmd, shell=True)
        mode_info = subprocess.check_output(mod_cmd, shell=True)
        testutils.test_logger.info("{0} : fbset display details. " .format(time.asctime()))
        testutils.test_logger.info(fb_info.decode('utf-8'))
        testutils.test_logger.info("{0} : Available IO display Interfaces. ".format(time.asctime()))
        testutils.test_logger.info(io_info.decode('utf-8'))
        testutils.test_logger.info("{0} : Display Mode Info. ".format(time.asctime()))
        testutils.test_logger.info(mode_info.decode('utf-8'))
        err_code = testutils.TEST_RESULT_PASS
        err_str = "{0} : All the Display Configs are available.".format(time.asctime())
        testutils.test_case_update_result(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : fb0 not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        testutils.test_logger.fatal(err_code, err_str)
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   03. Check External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   Renders a  -> Image on Display,
#              -> Performs Facial recog'tion from camera.
#
# # #

def render_program_display():

    try:
        import cv2

        f_path = "/dev/fb0"
        testutils.test_logger.info("{0} : Checking fbo status..".format(time.asctime()))

        if os.path.exists(f_path):

            testutils.test_logger.info("{0} : Triggering Camera Output." .format(time.asctime()))
            cap = cv2.VideoCapture(0)

            testutils.test_logger.info("{0} : Checking for Face Cascade .xml files..".format(time.asctime()))

            # Create the haar cascade
            if os.path.isfile("Contents/CV/haarcascade_frontalface_default.xml"):
                testutils.test_logger.info("{0} : Face Cascade file found!" .format(time.asctime()))
                faceCascade = cv2.CascadeClassifier("Contents/CV/haarcascade_frontalface_default.xml")

                while (True):
                    # Capture frame-by-frame
                    ret, frame = cap.read()

                    # Our operations on the frame come here
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Detect faces in the image
                    faces = faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(30, 30)
                        # flags = cv2.CV_HAAR_SCALE_IMAGE
                    )

                    testutils.test_logger.info("{0} : Detected - {1} faces!".format(time.asctime(), len(faces)))

                    # Draw a rectangle around the faces
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Display the resulting frame
                    cv2.imshow('Camera', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                # When everything done, release the capture
                cap.release()
                cv2.destroyAllWindows()
        else:
            testutils.test_logger.fatal("{0} : fb0 not available.".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
            testutils.test_logger.fatal(err_code, err_str)
            raise testutils.TestFailureException(err_code, err_str)

    except ImportError:
        testutils.test_logger.error("{0} : OpenCV package not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_ERROR
        err_str = "{0} : Test Failure - OpenCV package not available to Test. ".format(time.asctime())
        testutils.test_logger.error(err_code, err_str)
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   04. Check's External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   If fb0 is supported then performs below operations :
#                       -> Open a Image and read the colors from the images.
#                       -> Then create a color palette of all the colors read from the image.
#                       -> Once the Image is read displays it to the user.
#
# # #

def color_palette():
    img = "RC.png"
    img_path = "Contents/" + img
    testutils.test_logger.info("{0} : Looking for the Image.".format(time.asctime()))
    if os.path.exists(img_path):
        testutils.test_logger.info("{0} : Image found and reading the color.".format(time.asctime()))
        try:
            color_palette = subprocess.check_output("extcolors {0}" .format(img_path), shell=True)
            testutils.test_logger.info("R | G | B ::: Color Palette Details : \n" + color_palette.decode())
            for file in os.listdir():
                if file.startswith(img.replace(".png", "")):
                    testutils.test_logger.info("{0} : Color Palette Generate - " + file)
                    err_code = testutils.TEST_RESULT_PASS
                    err_str = "{0} : Color Palette Generated successfully.,".format(time.asctime())
                    testutils.test_case_update_result(err_code, err_str)
        except subprocess.CalledProcessError:
            testutils.test_logger.error("{0} : Execution Error, Try again.,, " .format(time.asctime()))
            err_code = testutils.TEST_RESULT_ERROR
            err_str = "{0} : Execution Error, Try again.,,".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : File not found - Cannot locate file.." .format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} :  File not found - Cannot locate file..".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   05. Check's External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   If fb0 is supported then performs below operations :
#                       -> To perform the control of brightness via backlight
#
# # #

def change_brightness():
    path = "/sys/class/backlight/intel_backlight/brightness"
    testutils.test_logger.info("{0} : Trying to change backlight brightness." .format(time.asctime()))
    backlight_range = [400, 1500, 6000, 3000, 400]
    if os.path.exists(path):
        testutils.test_logger.info("{0} : Supporting files available, proceeding to switch.." .format(time.asctime()))
        for brightness in backlight_range:
            try:
                testutils.test_logger.info("{0} : Switching to {1} - Brightness level".format(brightness, time.asctime()))
                subprocess.call("echo {0} | sudo tee {1}" .format(brightness, path),
                            shell=True)
                time.sleep(3)
                testutils.test_logger.info("{0} : Switched to {1} - Brightness level".format(brightness, time.asctime()))
            except subprocess.CalledProcessError:
                testutils.test_logger.error("{0} : Execution Error, Try again.,, ".format(time.asctime()))
                err_code = testutils.TEST_RESULT_ERROR
                err_str = "{0} : Execution Error, Try again.,,".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : File not found - Cannot find backlight files.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} :  File not found - Cannot find backlight files.".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   06. Check's External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   If fb0 is supported then performs below operations :
#   ->  process of overlaying a foreground image with transparency over a
#       background image. The transparency is often the fourth channel of an image
#       ( e.g. in a transparent PNG), but it can also be a separate image. This
#       transparency mask is often called the alpha mask or the alpha matte.
#
# # #

def alpha_blending():

    testutils.test_logger.info("{0} : Checking if Alpha Blending Images path exists.." .format(time.asctime()))

    people_path = os.getcwd() + "/Contents/Alpha/people.png"
    ocean_path = os.getcwd() + "/Contents/Alpha/ocean.jpg"
    mat_path = os.getcwd() + "/Contents/Alpha/mat.png"

    if os.path.exists(people_path) and os.path.exists(ocean_path) and os.path.exists(mat_path):

        testutils.test_logger.info("{0} : Images found in system path.. " .format(time.asctime()))

        foreground = cv2.imread(people_path)
        background = cv2.imread(ocean_path)
        alpha = cv2.imread(mat_path)

        foreground = foreground.astype(float)
        background = background.astype(float)

        alpha = alpha.astype(float) / 255

        foreground = cv2.multiply(alpha, foreground)
        background = cv2.multiply(1.0 - alpha, background)

        outImage = cv2.add(foreground, background)

        #img = cv2.imshow("OutImg", outImage/255)

        testutils.test_logger.info("{0} : Writing the output to a Image..." .format(time.asctime()))

        img = "Alpha_blending.png"

        cv2.imwrite(img, outImage)

        testutils.test_logger.info("{0} : Checking the written file.. " .format(time.asctime()))

        if os.path.exists(os.getcwd() + "/" + img):
            testutils.test_logger.info("{0} : Alpha Blending Image Generated Successfully.".format(time.asctime()))
            testutils.test_logger.info("{0} : Image Available location - {1}".format(time.asctime(), os.getcwd() + "/" + img))
        else:
            testutils.test_logger.error("{0} : Alpha Blending Image Generation Failure." .format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Test Failure - Alpha Blending Image Generation Failure.".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)

        cv2.waitKey(0)

    else:
        testutils.test_logger.fatal("{0} : Alpha Blending supporting files. Not Found!.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Images not found - Alpha Blending supporting files. Not Found!.".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   07. Check's External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   If fb0 is supported then performs below operations :
#   ->  Takes a input image and then performs the below functions:
#          -> Image Resize, for 25%, 50%, 100%, 150%, 250%..
#          -> Generate the Resize images and Save.
#
# # #

def img_scaling():

    img = "Retro"

    img_path = os.getcwd() + "/Contents/Resize/" + img + ".png"

    testutils.test_logger.info("{0} : Checking is Source Image is Available.. " .format(time.asctime()))

    if os.path.exists(img_path):

        testutils.test_logger.info("{0} : Source Image path found.." .format(time.asctime()))
        src = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

        scale_per = [50, 75, 150]

        for scale in scale_per:

            testutils.test_logger.info("{0} : Scaling Image to : {1}%" .format(time.asctime(), scale))
            width = int(src.shape[1] * scale / 100)
            height = int(src.shape[0] * scale / 100)

            dsize = (width, height)

            output = cv2.resize(src, dsize)
            testutils.test_logger.info("{0} : Writing the Scaled image to the output Image." .format(time.asctime()))
            cv2.imwrite(img + "_" + str(scale) + ".png", output)
            testutils.test_logger.info("{0} : Successfully written the Output image in location : "
                                       .format(time.asctime()) + img + "_" + str(scale) + ".png")

    #    cv2.waitKey(0)
    else:
        testutils.test_logger.fatal("{0} : Error :: Resizing - Source Image not found!".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Image not found - Source Image Not Found!.".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   08. Check's External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   If fb0 is supported then performs below operations :
#   ->  Checks the Connected Display and performs the following.:
#          -> Gets the EDID Data of the Connected Display.
#               (Ext, Display Identification Data..)
#
# # #

def get_edid():
    testutils.test_logger.info("{0} : Get the EDID Data of a Connected Display." .format(time.asctime()))
    try:
        #edid_data = subprocess.check_output("python3 -m hexdump /sys/class/drm/card0-eDP-1/edid", shell=True)
        edid_data = subprocess.check_output("python3 -m hexdump /sys/class/drm/card0-HDMI-A-1/edid", shell=True)
        testutils.test_logger.info("{0} : Getting the EDID Data.." .format(time.asctime()))
        testutils.test_logger.info('\n' * 2 + edid_data.decode())
        edid_file = open("EDID.txt", 'w+')
        edid_file.write(edid_data.decode())
        edid_file.close()
        testutils.test_logger.info("{0} : Checking if the EDID file is created.." .format(time.asctime()))
        if os.path.exists(os.getcwd() + "/EDID.txt"):
            testutils.test_logger.info("{0} : EDID file is created, and saved Successfully..".format(time.asctime()))
        else:
            testutils.test_logger.error("{0} : Error :: EDID Test Failure!" .format(time.asctime()))
            err_code = testutils.TEST_RESULT_ERROR
            err_str = "{0} : EDID Test Failure, Could not located Text File in path!." .format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    except subprocess.CalledProcessError:
        testutils.test_logger.fatal("{0} : Error :: EDID Test Failure!".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : EDID Test Failure, Cannot Execute Program!.".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   09. Check's External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   If fb0 is supported then performs below operations :
#   ->  Checks the Connected Display and performs the following.:
#          -> Takes Image as a Source and performs below functions.
#               ->  Pixel of Height and Width
#               ->  Outputs the Channels available..
#
# # #

def change_resolution():
    testutils.test_logger.skip("Skipping the Test...")
    testutils.test_logger.skip("{0} : Skipping the Test...".format(time.asctime()))
    err_code = testutils.TEST_RESULT_SKIP
    err_str = "{0} : Skipping the Test, Cannot Execute Program!.".format(time.asctime())
    raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   10. Check's External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   If fb0 is supported then performs below operations :
#   ->  Checks the Connected Display and performs the following.:
#          -> Takes Image as a Source and performs below functions.
#               ->  Pixel of Height and Width
#               ->  Outputs the Channels available..
#
# # #

def depth_change():
    testutils.test_logger.skip("Skipping the Test...")
    testutils.test_logger.skip("{0} : Skipping the Test...".format(time.asctime()))
    err_code = testutils.TEST_RESULT_SKIP
    err_str = "{0} : Skipping the Test, Cannot Execute Program!.".format(time.asctime())
    raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   11. Check's External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   If fb0 is supported then performs below operations :
#   ->  Checks the Connected Display and performs the following.:
#          -> Takes Image as a Source and performs below functions.
#               ->  Pixel of Height and Width
#               ->  Outputs the Channels available..
#
# # #

def get_img_info():
    pic = "Lion.jpg"
    img_path = os.getcwd() + "/Contents/" + pic

    testutils.test_logger.info("{0} : Checking for source Image.." .format(time.asctime()))

    if os.path.exists(img_path):
        testutils.test_logger.info("{0} : Source Image Path available." .format(time.asctime()))
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        size = img.size
        height, width, channels = img.shape[0], img.shape[1], img.shape[2]
        testutils.test_logger.info("{0} : {1} Image Information.. ".format(time.asctime(), pic))
        testutils.test_logger.info("{0} : Width : {1}" .format(time.asctime(), width))
        testutils.test_logger.info("{0} : Height : {1}".format(time.asctime(), height))
        testutils.test_logger.info("{0} : Pixels : {1}" .format(time.asctime(), height*width))
        testutils.test_logger.info("{0} : Size : {1}".format(time.asctime(), size))
        testutils.test_logger.info("{0} : Channels : {1}" .format(time.asctime(), channels))
    else:
        testutils.test_logger.fatal("{0} : Error :: Resizing - Source Image not found!".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Image not found - Source Image Not Found in Path!.".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   12. Check's External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   If fb0 is supported then performs below operations :
#   ->  Checks the Connected Display and performs the following.:
#          -> Takes Image as a Source and performs below functions.
#               ->  Changes the Color Depth of the image..
#                       By varying the cluster from 4, 8, 16, 32
#                       (higher the Value, better image color quality..)
# # #

def change_color_depth():

    def kmeans_color_quantization(image, clusters=4, rounds=1):
        testutils.test_logger.info("{0} : Getting the Image Sizes. " .format(time.asctime()))
        h, w = image.shape[0], image.shape[1]
        samples = np.zeros([h * w, 3], dtype=np.float32)
        count = 0
        for x in range(h):
            for y in range(w):
                samples[count] = image[x][y]
                count += 1
        compactness, labels, centers = cv2.kmeans(samples, clusters, None,
                                                  (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001),
                                                  rounds, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        res = centers[labels.flatten()]
        testutils.test_logger.info("{0} : Getting the Processed Image.. " .format(time.asctime()))
        return res.reshape(image.shape)

    img_path = os.getcwd() + "/Contents/" + "Bit.jpg"

    if os.path.exists(img_path):
        testutils.test_logger.info("{0} : Source Image path found." .format(time.asctime()))
        image = cv2.imread(img_path)
        testutils.test_logger.info("{0} : Processing Color Depth by Default set to : 4 Bit" .format(time.asctime()))
        result = kmeans_color_quantization(image, clusters=4)
        testutils.test_logger.info("{0} : Saving the Generated Image.." .format(time.asctime()))
        cv2.imwrite('Bit-4.jpg', result)
        testutils.test_logger.info("{0} : Image Saved Successfully.".format(time.asctime()))
        #cv2.waitKey()
        testutils.test_logger.info("{0} : Validating the processed Image.." .format(time.asctime()))
        if os.path.exists(os.getcwd()+"/Bit-4.jpg"):
            testutils.test_logger.info("{0} : Output processed Image, found." .format(time.asctime()))
        else:
            testutils.test_logger.fatal("{0} : Error :: Resizing - Source Image not found!".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Output Image not Found.!.".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.error("{0} : Error :: Resizing - Source Image not found!".format(time.asctime()))
        err_code = testutils.TEST_RESULT_ERROR
        err_str = "{0} : Image not found - Source Image Not Found in Path!.".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   13. Check's External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   If fb0 is supported then performs below operations :
#   ->  Checks the Connected Display and performs the following.:
#          -> Creates a Animated 2D Image and Renders it on the display.
#
# # #

def render_image():

    images = []

    testutils.test_logger.info("{0} : Setting up Parameters." .format(time.asctime()))

    width = 600
    center = width // 2
    color_1 = (0, 153, 153)
    color_2 = (0, 255, 255)
    max_radius = int(center * 1.5)
    step = 8

    testutils.test_logger.info("{0} : Trying to Import necessary libraries.. ".format(time.asctime()))
    try:
        from PIL import Image, ImageDraw
        import webbrowser

        testutils.test_logger.info("{0} : Libraries available..".format(time.asctime()))

        for i in range(0, max_radius, step):
            im = Image.new('RGB', (width, width), color_1)
            draw = ImageDraw.Draw(im)
            draw.ellipse((center - i, center - i, center + i, center + i), fill=color_2)
            images.append(im)

        for i in range(0, max_radius, step):
            im = Image.new('RGB', (width, width), color_2)
            draw = ImageDraw.Draw(im)
            draw.ellipse((center - i, center - i, center + i, center + i), fill=color_1)
            images.append(im)

        testutils.test_logger.info("{0} : Trying to save image. ".format(time.asctime()))

        images[0].save("Image.gif",
                       save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)

        if os.path.exists(os.getcwd() + "/Image.gif"):
            testutils.test_logger.info("{0} : Image saved Successfully.." .format(time.asctime()))
            #webbrowser.open("Image.gif")
        else:
            testutils.test_logger.error("{0} : Image generation failed. " .format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Image generation failed.".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)

    except ImportError:
        testutils.test_logger.fatal("{0} : Cannot Import Required Test Packages." .format(time.asctime()))
        err_code = testutils.TEST_RESULT_ERROR
        err_str = "{0} : Cannot Import Required Test Packages.".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   14. Check's External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   If fb0 is supported then performs below operations :
#   ->  Checks the Connected Display and performs the following.:
#          -> Creates a Overlap image from 2 images.
#
# # #

def overlay_support():

    img1_path = os.getcwd() + "/Contents/Overlay/1.jpg"
    img2_path = os.getcwd() + "/Contents/Overlay/2.jpg"

    testutils.test_logger.info("{0} : Checking if the Source Images are available. " .format(time.asctime()))

    if os.path.exists(img1_path) and os.path.exists(img2_path):

        try:
            from PIL import Image
            testutils.test_logger.info("{0} : Source Path Available in path." .format(time.asctime()))
            bg_img = Image.open(img1_path)
            ov_img = Image.open(img2_path)

            bg_img = bg_img.convert("RGBA")
            ov_img = ov_img.convert("RGBA")

            testutils.test_logger.info("{0} : Blending the source images.. " .format(time.asctime()))

            overlay_img = Image.blend(bg_img, ov_img, 0.5)

            overlay_img.save("Overlay.png", 'PNG')

            if os.path.exists(os.getcwd() + "/Overlay.png"):
                testutils.test_logger.info("{0} : Overlay Image Successfully created." .format(time.asctime()))
                testutils.test_logger.info("{0} : Overlay Image location : {1}" .format(time.asctime(),
                                                                                        os.getcwd()+"/Overlay.png"))
            else:
                testutils.test_logger.fatal("{0} : Cannot Import Required Test Packages.".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Cannot Import Required Test Packages.".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)

        except ImportError:
            testutils.test_logger.fatal("{0} : Cannot Import Required Test Packages.".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Cannot Import Required Test Packages.".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.error("{0} : Source Overlay images not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_ERROR
        err_str = "{0} : Source overlay images are not available.".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)



# Main functional Block..
if __name__ == '__main__':
    status = test_disp_main(sys.argv)
    sys.exit(status)
