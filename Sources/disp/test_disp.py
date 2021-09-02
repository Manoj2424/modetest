#!/usr/bin/python

#################################################################################
# File Name: test_disp.py                                                        #
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


# Import test specific utilities
sys.path.append('../common')
import testutils

# import validator

#################################################################################
# DISPLAY Constant Definitions                                                     #
#################################################################################
TOTAL_DISPLAY_TESTS = 50  # Total number of tests for DISPLAY IP
DISP_TEST_C_BINARY_FILE = './bin/test_disp'  # DISPLAY test binary file for executing test cases implemented in C
# TEST_DISPLAY_SUPP_BAUD_RATE    = [9600, 19200, 38400, 57600, 115200]
# TEST_DISPLAY_SUPP_DATA_BITS    = [5, 6, 7, 8]
# TEST_DISPLAY_SUPP_PARITY_BITS  = ['none', 'even', 'odd', 'mark', 'space']
# TEST_DISPLAY_SUPP_STOP_BITS    = ['1p0', '1p5', '2p0']

#################################################################################
# DISPLAY Global Variables                                                      #
#################################################################################
test_disp_setup_params = {}
test_disp_mode_params = {}
iteration = 1
# List of supported test cases for DISPLAY
test_disp_test_case_list = {
    1: 'NB2_DISP_01 (NB2_34) : Render Image on Display with Framebuffer.',
    2: 'NB2_DISP_02 (NB2_35 & NB2_36) : Display Interface, BPP and Resolution Info.',
    3: 'NB2_DISP_03 : Check Support for fb0',
    4: 'NB2_DISP_04 : Render a String on Framebuffer',
    5: 'NB2_DISP_05 : Write dmesg output to display buffer.',
    6: 'NB2_DISP_06 : Fb-Test (Color Palette)',
    7: 'NB2_DISP_07 : Fb-Test (Red - Non Palette)',
    8: 'NB2_DISP_08 : Fb-Test (Green - Non Palette)',
    9: 'NB2_DISP_09 : Fb-Test (Blue - Non Palette)',
    10: 'NB2_DISP_10 : Fb-Test (White - Non Palette)',
    11: 'NB2_DISP_11 : FB-Mark (SierpiSki)',
    12: 'NB2_DISP_12 : FB-Mark (Mandrolbrot)',
    13: 'NB2_DISP_13 : FB-Mark (Rectagle)',
    14: 'NB2_DISP_14 : Render Image on FB',
    15: 'NB2_DISP_15 : Render Image on FB',
    16: 'NB2_DISP_16 : Render Image on FB',
    17: 'NB2_DISP_17 : Render Image on FB.',
    18: 'NB2_DISP_18 : Display Rotate Framebuffer',
    19: 'NB2_DISP_19 : Display backlight or Brightness Control',
    20: 'NB2_DISP_20 : Modeset',
    21: 'NB2_DISP_21 : Modeset - Double buffer',
    22: 'NB2_DISP_22 : Modeset - vSync',
    23: 'NB2_DISP_23 : DRM Test – Read Display Frequency (vbltest)',
    24: 'NB2_DISP_24 : DRM Test – Change display resolution and frequency',
    25: 'NB2_DISP_25 : DRM Test – Support for Hardware Cursor.',
    26: 'NB2_DISP_26 : DRM Test – Support for vertical Sync.',
    27: 'NB2_DISP_27 : DRM Test – Validate support for Overlay.',
    28: 'NB2_DISP_28 : DRM Test – Support for Alpha Blending.',
    29: 'NB2_DISP_29 : DRM Test – vSync Page Flip with Resolution Change',
    30: 'NB2_DISP_30 : DRM Test – Hardware Cursor with Resolution Change',
    31: 'NB2_DISP_31 : DRM Test – HW Cursor + vSync Page Flip with Resolution Change'
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
    print("  -t <test_number>           NB2_DISP_01. (NB2_34) : Render Image on Display with Framebuffer", flush=True)
    print("                             NB2_DISP_02. (NB2_35 & NB2_36) : Display Interface, BPP and Resolution Info", flush=True)
    print("                             NB2_DISP_03. Check Support for fb0", flush=True)
    print("                             NB2_DISP_04. Render a String on Framebuffer", flush=True)
    print("                             NB2_DISP_05. Write dmesg output to display buffer", flush=True)
    print("                             NB2_DISP_06. Fb-Test (Color Palette)", flush=True)
    print("                             NB2_DISP_07. Fb-Test (Red - Non Palette)", flush=True)
    print("                             NB2_DISP_08. Fb-Test (Green - Non Palette)", flush=True)
    print("                             NB2_DISP_09. Fb-Test (Blue - Non Palette)", flush=True)
    print("                             NB2_DISP_10. Fb-Test (White - Non Palette).", flush=True)
    print("                             NB2_DISP_11. FB-Mark (SierpiSki)", flush=True)
    print("                             NB2_DISP_12. FB-Mark (Mandrolbrot)", flush=True)
    print("                             NB2_DISP_13. FB-Mark (Rectagle)", flush=True)
    print("                             NB2_DISP_14. Render Image on FB", flush=True)
    print("                             NB2_DISP_15. Render Image on FB", flush=True)
    print("                             NB2_DISP_16. Render Image on FB.", flush=True)
    print("                             NB2_DISP_17. Render Image on FB.", flush=True)
    print("                             NB2_DISP_18. Display Rotate Framebuffer.", flush=True)
    print("                             NB2_DISP_19. Display backlight or Brightness Control.", flush=True)
    print("                             NB2_DISP_20. Modeset.", flush=True)
    print("                             NB2_DISP_21. Modeset - Double buffer", flush=True)
    print("                             NB2_DISP_22. Modeset - vSync", flush=True)
    print("                             NB2_DISP_23. DRM Test – Read Display Frequency (vbltest)", flush=True)
    print("                             NB2_DISP_24. DRM Test – Change display resolution and frequency", flush=True)
    print("                             NB2_DISP_25. DRM Test – Support for Hardware Cursor", flush=True)
    print("                             NB2_DISP_26. DRM Test – Support for vertical Sync.", flush=True)
    print("                             NB2_DISP_27. DRM Test – Validate support for Overlay.", flush=True)
    print("                             NB2_DISP_28. DRM Test – Support for Alpha Blending.", flush=True)
    print("                             NB2_DISP_29. DRM Test – vSync Page Flip with Resolution Change", flush=True)
    print("                             NB2_DISP_30. DRM Test – Hardware Cursor with Resolution Change", flush=True)
    print("                             NB2_DISP_31. DRM Test – HW Cursor + vSync Page Flip with Resolution Change", flush=True)    
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
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_01 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                fb0_enabled()
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 2:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_02 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                get_display_info()
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 3:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_03 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                fb0_enabled()
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 4:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_04 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                fb_string()
                #random_screen()
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 5:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_05 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                log_to_console()

        elif test_case == 6:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_06 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                fbtest()
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 7:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_07 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                fbtest_param("-r")
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 8:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_08 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                fbtest_param("-g")
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 9:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or  not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_09 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                fbtest_param("-b")
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 10:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_10 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                fbtest_param("-w")
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 11:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_11 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                if check_display():
                    fb_sierpinski()
                else:
                    fb_sierpinski()
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 12:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_12 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                if check_display():
                    fb_mandelbrot()
                else:
                    fb_mandelbrot()
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 13:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_13 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                if check_display():
                    fb_rectangle()
                else:
                    fb_rectangle()
            #           Once called, returns an Error Code with the Error String
            #           Pass or Fail Message..

        elif test_case == 14:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_14 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                bpp = 'cat /sys/devices/platform/display-subsystem/graphics/fb0/bits_per_pixel'
                
                try:
                    testutils.test_logger.info("{0} Checking Display BPP Value." .format(time.asctime()))
                    bpp_val = subprocess.check_output(bpp, shell=True).decode('utf-8')
                    testutils.test_logger.info("{0} Current Display BPP Value - {1}" .format(time.asctime(), bpp_val))
                    if check_display():
                        if int(bpp_val) == 32:
                            render_images("LVDS", '/opt/lvds/32bpp/')
                        elif int(bpp_val) == 24:
                            render_images("LVDS", '/opt/lvds/24bpp/')    
                        elif int(bpp_val) == 16:
                            render_images("LVDS", '/opt/lvds/16bpp/')
                        else:
                            testutils.test_logger.error("{0} : Cannot locate LVDS image directory.".format(time.asctime()))
                            err_code = testutils.TEST_RESULT_ERROR
                            err_str = "{0} : Test Execution Failure..".format(time.asctime())
                            raise testutils.TestFailureException(err_code, err_str)
                    else:
                        if int(bpp_val) == 32:
                            render_images("MIPI", '/opt/mipi/32bpp/')
                        elif int(bpp_val) == 24:
                            render_images("MIPI", '/opt/mipi/24bpp/')    
                        elif int(bpp_val) == 16:
                            render_images("MIPI", '/opt/mipi/16bpp/')
                        else:
                            testutils.test_logger.error("{0} : Cannot locate MIPI image directory.".format(time.asctime()))
                            err_code = testutils.TEST_RESULT_ERROR
                            err_str = "{0} : Test Execution Failure..".format(time.asctime())
                            raise testutils.TestFailureException(err_code, err_str)
            #               Once called, returns an Error Code with the Error String
            #               Pass or Fail Message..
                except subprocess.CalledProcessError:
                    testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, cannot proceed.".format(time.asctime()))
                    err_code = testutils.TEST_RESULT_FATAL
                    err_str = "{0} : Test Cmd Execution Failure, cannot proceed.".format(time.asctime())
                    raise testutils.TestFailureException(err_code, err_str)

        elif test_case == 15:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_15 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                bpp = 'cat /sys/devices/platform/display-subsystem/graphics/fb0/bits_per_pixel'
                
                try:
                    testutils.test_logger.info("{0} Checking Display BPP Value." .format(time.asctime()))
                    bpp_val = subprocess.check_output(bpp, shell=True).decode('utf-8')
                    testutils.test_logger.info("{0} Current Display BPP Value - {1}" .format(time.asctime(), bpp_val))
                    if check_display():
                        if int(bpp_val) == 32:
                            render_images("LVDS", '/opt/lvds/32bpp/')
                        elif int(bpp_val) == 24:
                            render_images("LVDS", '/opt/lvds/24bpp/')    
                        elif int(bpp_val) == 16:
                            render_images("LVDS", '/opt/lvds/16bpp/')
                        else:
                            testutils.test_logger.error("{0} : Cannot locate LVDS image directory.".format(time.asctime()))
                            err_code = testutils.TEST_RESULT_ERROR
                            err_str = "{0} : Test Execution Failure..".format(time.asctime())
                            raise testutils.TestFailureException(err_code, err_str)
                    else:
                        if int(bpp_val) == 32:
                            render_images("MIPI", '/opt/mipi/32bpp/')
                        elif int(bpp_val) == 24:
                            render_images("MIPI", '/opt/mipi/24bpp/')    
                        elif int(bpp_val) == 16:
                            render_images("MIPI", '/opt/mipi/16bpp/')
                        else:
                            testutils.test_logger.error("{0} : Cannot locate MIPI image directory.".format(time.asctime()))
                            err_code = testutils.TEST_RESULT_ERROR
                            err_str = "{0} : Test Execution Failure..".format(time.asctime())
                            raise testutils.TestFailureException(err_code, err_str)
                            #Once called, returns an Error Code with the Error String
                            #Pass or Fail Message..
                except subprocess.CalledProcessError:
                    testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, cannot proceed.".format(time.asctime()))
                    err_code = testutils.TEST_RESULT_FATAL
                    err_str = "{0} : Test Cmd Execution Failure, cannot proceed.".format(time.asctime())
                    raise testutils.TestFailureException(err_code, err_str)
            
            
        elif test_case == 16:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_16 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                bpp = 'cat /sys/devices/platform/display-subsystem/graphics/fb0/bits_per_pixel'
                try:
                    testutils.test_logger.info("{0} Checking Display BPP Value." .format(time.asctime()))
                    bpp_val = subprocess.check_output(bpp, shell=True).decode('utf-8')
                    testutils.test_logger.info("{0} Current Display BPP Value - {1}" .format(time.asctime(), bpp_val))
                    if check_display():
                        if int(bpp_val) == 32:
                            render_images("LVDS", '/opt/lvds/32bpp/')
                        elif int(bpp_val) == 24:
                            render_images("LVDS", '/opt/lvds/24bpp/')    
                        elif int(bpp_val) == 16:
                            render_images("LVDS", '/opt/lvds/16bpp/')
                        else:
                            testutils.test_logger.error("{0} : Cannot locate LVDS image directory.".format(time.asctime()))
                            err_code = testutils.TEST_RESULT_ERROR
                            err_str = "{0} : Test Execution Failure..".format(time.asctime())
                            raise testutils.TestFailureException(err_code, err_str)
                    else:
                        if int(bpp_val) == 32:
                            render_images("MIPI", '/opt/mipi/32bpp/')
                        elif int(bpp_val) == 24:
                            render_images("MIPI", '/opt/mipi/24bpp/')    
                        elif int(bpp_val) == 16:
                            render_images("MIPI", '/opt/mipi/16bpp/')
                        else:
                            testutils.test_logger.error("{0} : Cannot locate MIPI image directory.".format(time.asctime()))
                            err_code = testutils.TEST_RESULT_ERROR
                            err_str = "{0} : Test Execution Failure..".format(time.asctime())
                            raise testutils.TestFailureException(err_code, err_str)
            #               Once called, returns an Error Code with the Error String
            #               Pass or Fail Message..      

                except subprocess.CalledProcessError:
                    testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, cannot proceed.".format(time.asctime()))
                    err_code = testutils.TEST_RESULT_FATAL
                    err_str = "{0} : Test Cmd Execution Failure, cannot proceed.".format(time.asctime())
                    raise testutils.TestFailureException(err_code, err_str)

        elif test_case == 17:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_17 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                bpp = 'cat /sys/devices/platform/display-subsystem/graphics/fb0/bits_per_pixel'
                try:
                    testutils.test_logger.info("{0} Checking Display BPP Value." .format(time.asctime()))
                    bpp_val = subprocess.check_output(bpp, shell=True).decode('utf-8')
                    testutils.test_logger.info("{0} Current Display BPP Value - {1}" .format(time.asctime(), bpp_val))
                    if check_display():
                        if int(bpp_val) == 32:
                            render_images("LVDS", '/opt/lvds/32bpp/')
                        elif int(bpp_val) == 24:
                            render_images("LVDS", '/opt/lvds/24bpp/')    
                        elif int(bpp_val) == 16:
                            render_images("LVDS", '/opt/lvds/16bpp/')
                        else:
                            testutils.test_logger.error("{0} : Cannot locate LVDS image directory.".format(time.asctime()))
                            err_code = testutils.TEST_RESULT_ERROR
                            err_str = "{0} : Test Execution Failure..".format(time.asctime())
                            raise testutils.TestFailureException(err_code, err_str)
                    else:
                        if int(bpp_val) == 32:
                            render_images("MIPI", '/opt/mipi/32bpp/')
                        elif int(bpp_val) == 24:
                            render_images("MIPI", '/opt/mipi/24bpp/')    
                        elif int(bpp_val) == 16:
                            render_images("MIPI", '/opt/mipi/16bpp/')
                        else:
                            testutils.test_logger.error("{0} : Cannot locate MIPI image directory.".format(time.asctime()))
                            err_code = testutils.TEST_RESULT_ERROR
                            err_str = "{0} : Test Execution Failure..".format(time.asctime())
                            raise testutils.TestFailureException(err_code, err_str)
            #               Once called, returns an Error Code with the Error String
            #               Pass or Fail Message.. 
                except subprocess.CalledProcessError:
                    testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, cannot proceed.".format(time.asctime()))
                    err_code = testutils.TEST_RESULT_FATAL
                    err_str = "{0} : Test Cmd Execution Failure, cannot proceed.".format(time.asctime())
                    raise testutils.TestFailureException(err_code, err_str)
                    
        elif test_case == 18:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_18 : Test Iteration : {1} ═══════════"
                        .format(time.asctime(), idx))
                rotate_screen()
                
        elif test_case == 19:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_19 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                change_brightness()

        elif test_case == 20:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_20 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                modeset()

        elif test_case == 21:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_21 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                modeset_double_buff()

        elif test_case == 22:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_22 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                modeset_vsync()

        elif test_case == 23:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_23 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                change_brightness()

        elif test_case == 24:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_24 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                change_brightness()

        elif test_case == 25:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_25 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                change_brightness()

        elif test_case == 26:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_26 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                change_brightness()

        elif test_case == 27:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_27 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                change_brightness()

        elif test_case == 28:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_28 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                change_brightness()

        elif test_case == 29:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_29 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                change_brightness()
                
        elif test_case == 30:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_30 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                change_brightness()

        elif test_case == 31:
            #           Calling the Test Function directly..
            #           Test Case to check if the Graphics - Driver is loaded or not..
            for idx in range(1, iteration + 1):
                testutils.test_logger.info("{0} ═══════════ TEST_ID :: NB2_DISP_31 : Test Iteration : {1} ═══════════"
                                           .format(time.asctime(), idx))
                change_brightness()

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


#########################################################################################
#
#
#   ModeTest Parser Functions..
#           * To Compute Output Functions..
#           * Get Display Connection status
#           * Get CRTCs connection status..
#           * Gets vbltest connection status..
#           * Get DRM driver status..
#
#
#
#################################################################################################

def check_drm_status():
    try:
        drm = subprocess.check_output("modetest -d | grep done", shell=True)
        testutils.test_logger.info("{0} : Checking DRM Driver available status for ModeTest.." .format(time.asctime()))
        if b'done' in drm:
            testutils.test_logger.info("{0} : DRM Driver available.".format(time.asctime()))
            testutils.test_logger.info("{0} : DRM Driver - \n {1}".format(time.asctime(), drm.decode('utf-8')))
            return True
        else:
            testutils.test_logger.info("{0} : DRM Driver Not Found!".format(time.asctime()))
            return False
    except subprocess.CalledProcessError:
        testutils.test_logger.error("{0} : Failed to Execute Command." .format(time.asctime()))
        return False


def vbltest_status():
    try:
        vbl = subprocess.check_output("vbltest -s | grep done", shell=True)
        testutils.test_logger.info("{0} : Checking DRM Driver available status for Vbltest.." .format(time.asctime()))
        if b'done' in vbl:
            testutils.test_logger.info("{0} : DRM Driver available.".format(time.asctime()))
            testutils.test_logger.info("{0} : DRM Supported Driver - {1}".format(time.asctime(), vbl.decode('utf-8')))
            return True
        else:
            testutils.test_logger.info("{0} : DRM Driver Not Found!".format(time.asctime()))
            return False
    except subprocess.CalledProcessError:
        testutils.test_logger.error("{0} : Failed to Execute Command." .format(time.asctime()))
        return False


def hdmi_status():
    try:
        dis_status = subprocess.check_output("cat /sys/class/drm/card1-HDMI-A-1/status", shell=True)
        testutils.test_logger.info("{0} : Check Display Connection status.." .format(time.asctime()))
        if str(dis_status) == "b'connected\\n'":
            testutils.test_logger.info("{0} : HDMI display Interface - {1}.".format(time.asctime(),
                                                                            dis_status.decode('utf-8')))
            return True
        else:
            testutils.test_logger.info("{0} : HDMI display Interface : {1}.".format(time.asctime(),
                                                                                    dis_status.decode('utf-8')))
            return False
    except subprocess.CalledProcessError:
        testutils.test_logger.error("{0} : Failed to Execute HDMI Status Command.")
        return False


def connection_status():
    try:
        conn_info = subprocess.check_output("modetest | grep connected", shell=True)
        crtc = subprocess.check_output("modetest | grep -A3 CRTCs", shell=True)
        testutils.test_logger.info("{0} : Checking Active Display Connected, and CRTC "
                                   "Details..".format(time.asctime()))
        if b"connected" in conn_info and b"CRTCs" in crtc:
            testutils.test_logger.info("{0} : Display Connection and CRTC data Available.".format(time.asctime()))
            return conn_info, crtc
        else:
            testutils.test_logger.info("{0} : No Active Displays or CRTC found.".format(time.asctime()))
            return False, False
    except subprocess.CalledProcessError:
        testutils.test_logger.error("{0} : Failed to Execute Command." .format(time.asctime()))
        return False, False


def get_connector_and_crtc_modeprint():
    try:
        connector_info = subprocess.check_output("modeprint vc4 | grep -A1 Connector:", shell=True)
        crtc_info = subprocess.check_output("modeprint vc4 | grep -A1 Crtc", shell=True)

        if b"Connector:" in connector_info and b"id" in crtc_info:
            testutils.test_logger.info("{0} : Display Connection and CRTC data Available.".format(time.asctime()))
            connector = connector_info.decode('utf-8')
            connector = connector[-3:-1]
            testutils.test_logger.info("{0} : Connector ID : {1}" .format(time.asctime(), connector))
            crtc_id = crtc_info.decode('utf-8')
            crtc_id = crtc_id[-3:-1]
            testutils.test_logger.info("{0} : CRTC ID : {1}".format(time.asctime(), crtc_id))
            return connector, crtc_id
        else:
            testutils.test_logger.info("{0} : No Active Displays or CRTC found.".format(time.asctime()))
            return False, False
    except subprocess.CalledProcessError:
        testutils.test_logger.error("{0} : Failed to Execute Command.".format(time.asctime()))
        return False, False


def get_plane_id():
    try:
        connector_info = subprocess.check_output("modeprint vc4 | grep -A1 Connector:", shell=True)
        crtc_info = subprocess.check_output("modeprint vc4 | grep -A1 Crtc", shell=True)

        if b"Connector:" in connector_info and b"id" in crtc_info:
            testutils.test_logger.info("{0} : Display Connection and CRTC data Available.".format(time.asctime()))
            try:
                testutils.test_logger.info("{0} : Trying to get Display Plane ID." .format(time.asctime()))
                plane = subprocess.check_output("modetest -M vc4 | grep -A2 Planes:", shell=True)
                plane_id = plane[58:-36].decode('utf-8')
                testutils.test_logger.info("{0} : Verifying not Null Value.., "
                                           "Fetched Plane ID : '{1}'".format(time.asctime(), plane_id))
                if plane_id != "":
                    testutils.test_logger.info("{0} : Connected Display Plane ID : {1}" .format(time.asctime(), plane_id))
                    return plane_id
                else:
                    testutils.test_logger.error("{0} : Invalid Plane ID located : Null '{1}''".format(time.asctime(),
                                                                                                     plane_id))
                    return False
            except subprocess.CalledProcessError:
                testutils.test_logger.error("{0} : Failed to Execute Command.".format(time.asctime()))
                return False

    except subprocess.CalledProcessError:
        testutils.test_logger.error("{0} : Failed to Execute Command.".format(time.asctime()))
        return False


def is_kmscube_installed():
    try:
        apt_list = subprocess.check_output("dpkg --list  | grep kmscube", shell=True)
        testutils.test_logger.info("{0} : Checking if KMSCube available, to validate..".format(time.asctime()))
        if b"kmscube" in apt_list:
            testutils.test_logger.info("{0} : KMSCube available in the System.".format(time.asctime()))
            return True
        else:
            testutils.test_logger.info("{0} : No Active Displays or CRTC found.".format(time.asctime()))
            return False
    except subprocess.CalledProcessError:
        testutils.test_logger.error("{0} : Failed to Execute Command." .format(time.asctime()))
        return False


def fb_modes_available():
    fb_modes = "/etc/fb.modes"
    testutils.test_logger.info("{0} : Checking if Framebuffer Modes are Available.." .format(time.asctime()))
    if os.path.exists(fb_modes):
        testutils.test_logger.info("{0} : Framebuffer Modes available in the System.".format(time.asctime()))
        return True
    else:
        testutils.test_logger.info("{0} : Framebuffer Modes not found.".format(time.asctime()))
        return False


# # #
#
#   01. Check fb0 enabled..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#
# # #

def fb0_enabled():
    path = "/dev/fb0"
    testutils.test_logger.info("{0} : Checking fb0 status.." .format(time.asctime()))
    if os.path.exists(path):
        testutils.test_logger.info("{0} : fb0 found in path (/dev/fb0) in the System." .format(time.asctime()))
        err_code = testutils.TEST_RESULT_PASS
        err_str = "{0} : fb0 Framebuffer Device available." .format(time.asctime())
        testutils.test_case_update_result(err_code, err_str)
        return True
    else:
        testutils.test_logger.fatal("{0} : fb0 not available." .format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' Framebuffer not available in path. " .format(time.asctime())
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
        try:
            start_time = time.time()
            fb_info = subprocess.check_output("fbset", shell=True)
            io_info = subprocess.check_output(io_cmd, shell=True)
            mode_info = subprocess.check_output(mod_cmd, shell=True)
            end_time = time.time()
            testutils.test_logger.info("{0} : fbset display details. " .format(time.asctime()))
            testutils.test_logger.info(fb_info.decode('utf-8'))
            testutils.test_logger.info("{0} : Available IO display Interfaces. ".format(time.asctime()))
            testutils.test_logger.info(io_info.decode('utf-8'))
            testutils.test_logger.info("{0} : Display Mode Info. ".format(time.asctime()))
            testutils.test_logger.info(mode_info.decode('utf-8'))
            err_code = testutils.TEST_RESULT_PASS
            err_str = "{0} : All the Display Configs are available.".format(time.asctime())
            testutils.test_logger.info("{0} : Total Execution time - {1} secs..".format(time.asctime(),
                                                                                        end_time-start_time))
            testutils.test_case_update_result(err_code, err_str)
        except subprocess.CalledProcessError:
            testutils.test_logger.fatal("{0} : Test Execution Failure, Cannot proceed..".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Test Execution Failure, Cannot proceed.. ".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : fb0 not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   03. Check External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   Prints the -> Display Resolution,
#              -> Display Supported Interfaces, and their status.
#
# # #

def log_to_console():
    testutils.test_logger.info("{0} : Checking if Framebuffer device (fb0) is available.".format(time.asctime()))
    if fb0_enabled:
        testutils.test_logger.info("{0} : Framebuffer (fb0) device is available.".format(time.asctime()))
        cmd = "dmesg > /dev/tty1"
        testutils.test_logger.info("{0} : Proceeding test execution...".format(time.asctime()))
        try:
            ret = subprocess.call(cmd, shell=True)
            if ret == 0:
                testutils.test_logger.info("{0} : Test completed successfully..".format(time.asctime()))
            else:
                testutils.test_logger.fatal("{0} : Test Execution failure.".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Test Execution Failure..".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)
        except subprocess.CalledProcessError:
            testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : fb0 not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   04. Check External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   Prints the -> Display Resolution,
#              -> Display Supported Interfaces, and their status.
#
# # #

def random_screen():
    testutils.test_logger.info("{0} : Checking if Framebuffer device (fb0) is available.".format(time.asctime()))
    if fb0_enabled:
        testutils.test_logger.info("{0} : Framebuffer (fb0) device is available.".format(time.asctime()))
        urand = "dd if=/dev/urandom of=/dev/fb0"
        clear = "dd if=/dev/zero of=/dev/fb0"
        testutils.test_logger.info("{0} : Proceeding test execution.".format(time.asctime()))
        try:
            testutils.test_logger.info("{0} : Printing Random Data on the Display - {1}".format(time.asctime(), urand))
            urand_ret = subprocess.call(urand, shell=True)
            time.sleep(5)
            testutils.test_logger.info("{0} : Clear the Display Screen - {1}".format(time.asctime(), clear))
            clear_ret = subprocess.call(urand, shell=True)
            if urand_ret and clear_ret == 0:
                testutils.test_logger.info("{0} : Test completed successfully..".format(time.asctime()))
            else:
                testutils.test_logger.fatal("{0} : Test Failure, with Exit Codes {1} & {2}.".format(time.asctime(),
                                                                                                    urand_ret, clear_ret))
                testutils.test_logger.fatal("{0} : Test Execution failure.".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Test Execution Failure..".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)
        except subprocess.CalledProcessError:
            testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : fb0 not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   05. Check External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   Prints the -> Display Resolution,
#              -> Display Supported Interfaces, and their status.
#
# # #

def rotate_screen():
    testutils.test_logger.info("{0} : Checking if Framebuffer device (fb0) is available.".format(time.asctime()))
    if fb0_enabled:
        testutils.test_logger.info("{0} : Framebuffer (fb0) device is available.".format(time.asctime()))
        for var in range(0, 3):
            cmd = "echo " + str(var) + " > /sys/class/graphics/fbcon/rotate"
            testutils.test_logger.info("{0} : Proceeding test execution for Rotate - {1}..".format(time.asctime(), cmd))
            try:
                ret = subprocess.call(cmd, shell=True)
                time.sleep(10)
                if ret == 0:
                    testutils.test_logger.info("{0} : Test completed successfully for Rotate - {1}."
                                               "".format(time.asctime(), var))
                else:
                    testutils.test_logger.fatal("{0} : Test Execution failure.".format(time.asctime()))
                    err_code = testutils.TEST_RESULT_FATAL
                    err_str = "{0} : Test Execution Failure..".format(time.asctime())
                    raise testutils.TestFailureException(err_code, err_str)
            except subprocess.CalledProcessError:
                testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, fbcon unavailable cannot proceed.".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Test Cmd Execution Failure, fbcon unavailable cannot proceed.".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : fb0 not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   06. Check External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   Prints the -> Display Resolution,
#              -> Display Supported Interfaces, and their status.
#
# # #

def fb_string():
    testutils.test_logger.info("{0} : Checking if Framebuffer device (fb0) is available.".format(time.asctime()))
    if fb0_enabled:
        testutils.test_logger.info("{0} : Framebuffer (fb0) device is available.".format(time.asctime()))
        strings = ["NB2 Linux BSP!", "NB2 Linux BSP - ExaleapSemi", "NB2 Linux BSP - ExaleapSemi DisplaySS"]
        for string in strings:
            cmd = "fbstring 120 100 " + '"' + str(string) + '"' + " 0xff 0"
            cmd1 = "fbstring 120 100 " + '"' + str(string) + '"' + " 0xffff 0"
            try:
                testutils.test_logger.info("{0} : Proceeding test execution for String - {1}.".format(time.asctime(),
                                                                                                      cmd))
                ret = subprocess.call(cmd, shell=True)
                time.sleep(5)
                testutils.test_logger.info("{0} : Proceeding test execution for String - {1}.".format(time.asctime(),
                                                                                                      cmd1))
                ret1 = subprocess.call(cmd1, shell=True)
                time.sleep(5)
                if ret == 0 and ret1 == 0:
                    testutils.test_logger.info("{0} : Test completed successfully for FbString - {1}."
                                               "".format(time.asctime(), string))
                else:
                    testutils.test_logger.fatal("{0} : Test Execution failure.".format(time.asctime()))
                    err_code = testutils.TEST_RESULT_FATAL
                    err_str = "{0} : Test Execution Failure..".format(time.asctime())
                    raise testutils.TestFailureException(err_code, err_str)
            except subprocess.CalledProcessError:
                testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : fb0 not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   07. Check External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   Prints the -> Display Resolution,
#              -> Display Supported Interfaces, and their status.
#
# # #

def fbtest():
    testutils.test_logger.info("{0} : Checking if Framebuffer device (fb0) is available.".format(time.asctime()))
    if fb0_enabled:
        testutils.test_logger.info("{0} : Framebuffer (fb0) device is available.".format(time.asctime()))
        cmd = "fbtest 260x260+740-+480"
        testutils.test_logger.info("{0} : Proceeding test execution for FbTest - {1}.".format(time.asctime(),
                                                                                                   cmd))
        try:
            ret = subprocess.call(cmd, shell=True)
            if ret == 0:
                testutils.test_logger.info("{0} : Test completed successfully for FbTest - {1}.".format(time.asctime(),
                                                                                                        cmd))
            else:
                testutils.test_logger.fatal("{0} : Test Execution failure.".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Test Execution Failure..".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)
        except subprocess.CalledProcessError:
            testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : fb0 not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   08-11. Check External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   Prints the -> Display Resolution,
#              -> Display Supported Interfaces, and their status.
#
# # #

def fbtest_param(args):
    testutils.test_logger.info("{0} : Checking if Framebuffer device (fb0) is available.".format(time.asctime()))
    if fb0_enabled:
        testutils.test_logger.info("{0} : Framebuffer (fb0) device is available.".format(time.asctime()))
        cmd = "fbtest " + str(args)
        testutils.test_logger.info("{0} : Proceeding test execution for FbTest - {1}.".format(time.asctime(), cmd))
        try:
            ret = subprocess.call(cmd, shell=True)
            if ret == 0:
                testutils.test_logger.info("{0} : Test completed successfully for FbTest - {1}.".format(time.asctime(),
                                                                                                        cmd))
            else:
                testutils.test_logger.fatal("{0} : Test Execution failure.".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Test Execution Failure..".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)
        except subprocess.CalledProcessError:
            testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : fb0 not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#       **** CHECK SUM FUNCTION ***
#   *.Check Display Connectivity in use.*
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   Prints the -> Display Resolution,
#              -> Display Supported Interfaces, and their status.
#
# # #

def check_display():
    testutils.test_logger.info("{0} : Checking if the connected Display is LVDS or MIPI.".format(time.asctime()))
    try:
        display = subprocess.check_output('for p in /sys/class/drm/*/status; do con=${p%/status}; echo -n'
                                          ' "${con#*/card?-}: "; cat $p; done', shell=True)
        if b"LVDS" in display:
            testutils.test_logger.info("{0} : LVDS Display, connected.".format(time.asctime()))
            return True
        elif b"DSI" in display:
            testutils.test_logger.info("{0} : MIPI Display, connected.".format(time.asctime()))
            return False
        else:
            testutils.test_logger.fatal("{0} : Error checking the Display connection..".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Error checking the Display connection..".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    except subprocess.CalledProcessError:
        testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   11. Check External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   Prints the -> Display Resolution,
#              -> Display Supported Interfaces, and their status.
#
# # #

def fb_sierpinski():
    testutils.test_logger.info("{0} : Checking if Framebuffer device (fb0) is available.".format(time.asctime()))
    if fb0_enabled:
        testutils.test_logger.info("{0} : Framebuffer (fb0) device is available.".format(time.asctime()))
        cmd = " fb_sierpinski"
        testutils.test_logger.info("{0} : Proceeding test execution for Cmd - {1}.".format(time.asctime(), cmd))
        try:
            ret = subprocess.call(cmd, shell=True)
            if ret == 0:
                testutils.test_logger.info("{0} : Test completed successfully for fb_sierpinski - {1}.".format(time.asctime(),
                                                                                                        cmd))
            else:
                testutils.test_logger.fatal("{0} : Test Execution failure.".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Test Execution Failure..".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)
        except subprocess.CalledProcessError:
            testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : fb0 not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   12. Check External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   Prints the -> Display Resolution,
#              -> Display Supported Interfaces, and their status.
#
# # #

def fb_mandelbrot():
    testutils.test_logger.info("{0} : Checking if Framebuffer device (fb0) is available.".format(time.asctime()))
    if fb0_enabled:
        testutils.test_logger.info("{0} : Framebuffer (fb0) device is available.".format(time.asctime()))
        cmd = " fb_mandelbrot"
        testutils.test_logger.info("{0} : Proceeding test execution for Cmd - {1}.".format(time.asctime(), cmd))
        try:
            ret = subprocess.call(cmd, shell=True)
            if ret == 0:
                testutils.test_logger.info("{0} : Test completed successfully for fb_mandelbrot - {1}.".format(time.asctime(),
                                                                                                        cmd))
            else:
                testutils.test_logger.fatal("{0} : Test Execution failure.".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Test Execution Failure..".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)
        except subprocess.CalledProcessError:
            testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : fb0 not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   13. Check External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   Prints the -> Display Resolution,
#              -> Display Supported Interfaces, and their status.
#
# # #

def fb_rectangle():
    testutils.test_logger.info("{0} : Checking if Framebuffer device (fb0) is available.".format(time.asctime()))
    if fb0_enabled:
        testutils.test_logger.info("{0} : Framebuffer (fb0) device is available.".format(time.asctime()))
        cmd = "fb_rectangle"
        testutils.test_logger.info("{0} : Proceeding test execution for Cmd - {1}.".format(time.asctime(), cmd))
        try:
            ret = subprocess.call(cmd, shell=True)
            if ret == 0:
                testutils.test_logger.info("{0} : Test completed successfully for fb_rectangle - {1}.".format(time.asctime(),
                                                                                                        cmd))
            else:
                testutils.test_logger.fatal("{0} : Test Execution failure.".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Test Execution Failure..".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)
        except subprocess.CalledProcessError:
            testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : fb0 not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# # #
#
#   14. Check External Connectivity..
#   Checks if the 'fb0' in supported on devices /dev/fb0 directory..
#   Prints the -> Display Resolution,
#              -> Display Supported Interfaces, and their status.
#
# # #

def render_images(disp, path):
    testutils.test_logger.info("{0} : Checking the path to render Images on {1}.".format(time.asctime(), disp))
    if os.path.exists(path):
        testutils.test_logger.info("{0} : {1} binary path available, proceeding to test.".format(time.asctime(), disp))
        bins = os.listdir(path)
        testutils.test_logger.info("{0} : Found binaries in path - {1}".format(time.asctime(), bins))
        random.shuffle(bins)
        for bin in bins[:4]:
            cmd = "cat " + path + bin + " > /dev/fb0"
            try:
                testutils.test_logger.info("{0} : Trying to Execute the Cmd - {1}".format(time.asctime(), cmd))
                ret = subprocess.call(cmd, shell=True)
                time.sleep(10)
                if ret == 0:
                    testutils.test_logger.info("{0} : Test completed successfully for Rendering Image - {1}.".format(time.asctime(),
                                                                                         bin))
                else:
                    testutils.test_logger.fatal("{0} : Test Execution failure.".format(time.asctime()))
                    err_code = testutils.TEST_RESULT_FATAL
                    err_str = "{0} : Test Execution Failure..".format(time.asctime())
                    raise testutils.TestFailureException(err_code, err_str)
            except subprocess.CalledProcessError:
                testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)


def modeset():
    testutils.test_logger.info("{0} : Checking if Framebuffer device (fb0) is available.".format(time.asctime()))
    if fb0_enabled:
        testutils.test_logger.info("{0} : Framebuffer (fb0) device is available.".format(time.asctime()))
        cmd = "modeset"
        testutils.test_logger.info("{0} : Proceeding test execution for Modeset - {1}.".format(time.asctime(),
                                                                                                   cmd))
        try:
            ret = subprocess.call(cmd, shell=True)
            if ret == 0:
                testutils.test_logger.info("{0} : Test completed successfully for modeset - {1}.".format(time.asctime(),
                                                                                                        cmd))
            else:
                testutils.test_logger.fatal("{0} : Test Execution failure.".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Test Execution Failure..".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)
        except subprocess.CalledProcessError:
            testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : modeset not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


def modeset_double_buff():
    testutils.test_logger.info("{0} : Checking if Framebuffer device (fb0) is available.".format(time.asctime()))
    if fb0_enabled:
        testutils.test_logger.info("{0} : Framebuffer (fb0) device is available.".format(time.asctime()))
        cmd = "modeset-double-buffered"
        testutils.test_logger.info("{0} : Proceeding test execution for Modeset - {1}.".format(time.asctime(),
                                                                                                   cmd))
        try:
            ret = subprocess.call(cmd, shell=True)
            if ret == 0:
                testutils.test_logger.info("{0} : Test completed successfully for modeset - {1}.".format(time.asctime(),
                                                                                                        cmd))
            else:
                testutils.test_logger.fatal("{0} : Test Execution failure.".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Test Execution Failure..".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)
        except subprocess.CalledProcessError:
            testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : modeset not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


def modeset_vsync():
    testutils.test_logger.info("{0} : Checking if Framebuffer device (fb0) is available.".format(time.asctime()))
    if fb0_enabled:
        testutils.test_logger.info("{0} : Framebuffer (fb0) device is available.".format(time.asctime()))
        cmd = "modeset-vsync"
        testutils.test_logger.info("{0} : Proceeding test execution for Modeset - {1}.".format(time.asctime(),
                                                                                                   cmd))
        try:
            ret = subprocess.call(cmd, shell=True)
            if ret == 0:
                testutils.test_logger.info("{0} : Test completed successfully for modeset - {1}.".format(time.asctime(),
                                                                                                        cmd))
            else:
                testutils.test_logger.fatal("{0} : Test Execution failure.".format(time.asctime()))
                err_code = testutils.TEST_RESULT_FATAL
                err_str = "{0} : Test Execution Failure..".format(time.asctime())
                raise testutils.TestFailureException(err_code, err_str)
        except subprocess.CalledProcessError:
            testutils.test_logger.fatal("{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime()))
            err_code = testutils.TEST_RESULT_FATAL
            err_str = "{0} : Test Cmd Execution Failure, Cannot proceed..".format(time.asctime())
            raise testutils.TestFailureException(err_code, err_str)
    else:
        testutils.test_logger.fatal("{0} : modeset not available.".format(time.asctime()))
        err_code = testutils.TEST_RESULT_FATAL
        err_str = "{0} : Test Failure - 'fb0' not available in path. ".format(time.asctime())
        raise testutils.TestFailureException(err_code, err_str)


# Main functional Block..
if __name__ == '__main__':
    status = test_disp_main(sys.argv)
    sys.exit(status)
