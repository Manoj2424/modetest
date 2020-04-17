#!/usr/bin/python

#################################################################################
# File Name: testutils.py                                                       #
# Description: Python test utility file                                         #
# Author: Ganesh Shanubhogue (DevSys)                                           #
# Last Modified: 10-Feb-2020                                                    #
#                                                                               #
# Copyright: (c) 2019 ExaLeap.                                                  #
# ExaLeap Proprietary and Confidential. All rights reserved.                    #
#################################################################################
import logging
import sys
import subprocess
import time
import shlex

#################################################################################
# Test Failure Handling Exception                                               #
#################################################################################
class TestFailureException(Exception):
    def __init__(self, err_code, err_str):
        self.err_code = err_code
        self.err_str = err_str
    def __str__(self):
        return '{0} ({1})'.format(self.err_str, self.err_code)

#################################################################################
# Test Message Logger                                                           #
#################################################################################
# Terminal colors for the messages
COLOR_NORMAL    = '\x1b[0m'
COLOR_RED       = '\x1b[31m'
COLOR_GREEN     = '\x1b[32m'
COLOR_YELLOW    = '\x1b[33m'
COLOR_BLUE      = '\x1b[34m'
COLOR_MAGENTA   = '\x1b[35m'
COLOR_CYAN      = '\x1b[36m'
COLOR_WHITE     = '\x1b[37m'
TEST_LOG_FORMAT = 'TEST_%(levelname)s: %(filename)s:%(lineno)d:%(funcName)s(): %(message)s'
logging.basicConfig(stream=sys.stderr, format=TEST_LOG_FORMAT)
test_logger = logging.getLogger(__name__)
# Custom Log Levels
LOGGER_LEVEL_NOTICE = 33
LOGGER_LEVEL_SKIP = 36
LOGGER_LEVEL_FATAL = 55
# Logging Notice
logging.addLevelName(LOGGER_LEVEL_NOTICE, "NOTICE")
def test_logger_notice(self, message, *args, **kwargs):
    if self.isEnabledFor(LOGGER_LEVEL_NOTICE):
        self._log(LOGGER_LEVEL_NOTICE, message, args, **kwargs)
logging.Logger.notice = test_logger_notice
# Logging Skip
logging.addLevelName(LOGGER_LEVEL_SKIP, "SKIP")
def test_logger_skip(self, message, *args, **kwargs):
    if self.isEnabledFor(LOGGER_LEVEL_SKIP):
        self._log(LOGGER_LEVEL_SKIP, message, args, **kwargs)
logging.Logger.skip = test_logger_skip
# Logging Fatal
logging.addLevelName(LOGGER_LEVEL_FATAL, "FATAL")
def test_logger_fatal(self, message, *args, **kwargs):
    if self.isEnabledFor(LOGGER_LEVEL_FATAL):
        self._log(LOGGER_LEVEL_FATAL, message, args, **kwargs)
logging.Logger.fatal = test_logger_fatal
# Valid log level options:
#  NOTSET (0), DEBUG (10), INFO (20), WARNING (30), NOTICE (33), SKIP (36), ERROR (40), CRITICAL (50) or FATAL (55)
test_logger.setLevel(logging.DEBUG)
# Add color feature to the messages
def test_add_term_color(func):
    # Add methods we need to the class
    def new(*args):
        level = args[1].levelno
        if level >= LOGGER_LEVEL_FATAL:
            color = COLOR_RED
        elif level >= logging.CRITICAL:
            color = COLOR_RED
        elif level >= logging.ERROR:
            color = COLOR_RED
        elif level >= LOGGER_LEVEL_SKIP:
            color = COLOR_BLUE
        elif level >= LOGGER_LEVEL_NOTICE:
            color = COLOR_MAGENTA
        elif level >= logging.WARNING:
            color = COLOR_CYAN
        elif level >= logging.INFO:
            color = COLOR_NORMAL
        elif level >= logging.DEBUG:
            color = COLOR_NORMAL
        else:
            color = COLOR_NORMAL
        args[1].msg = color + args[1].msg + COLOR_NORMAL
        return func(*args)
    return new
logging.StreamHandler.emit = test_add_term_color(logging.StreamHandler.emit)

#################################################################################
# Test Result Codes                                                             #
#################################################################################
TEST_RESULT_PASS        = 0     # Test case is successful in all means
TEST_RESULT_WARNING     = 1     # Warning (not a failure), requires attention
TEST_RESULT_NOTICE      = 2     # Minor failure (test continues), but treated as failure
TEST_RESULT_SKIP        = 3     # Test skipped to execute, because of unimplemented/unsupported feature/scenario
TEST_RESULT_ERROR       = 4     # Test program error (not a IP failure), test code required to handle this scenario
TEST_RESULT_CRITICAL    = 5     # Actual failur (test stops), treated as failure (other tests can continue on IP)
TEST_RESULT_FATAL       = 6     # Major failure (test abandons), other tests can't continue on IP

#################################################################################
# Test Utils Constant Definitions                                               #
#################################################################################
TEST_SUITE_REPORT_FILE  = '.test_suite_report'      # Test report file for the complete test suite
TEST_CASE_REPORT_FILE   = '.test_case_report'       # Test report file for the individual test case from C

#################################################################################
# Test Utils Global Variables                                                   #
#################################################################################
test_suite_result_code = TEST_RESULT_PASS
test_case_result_code = TEST_RESULT_PASS
test_case_result_str = None
test_random_seed = 0

#################################################################################
# Test Utils Helper Methods                                                     #
#################################################################################
# Helper method to wait requested number of seconds
def test_wait_secs(wait_secs):
    test_logger.debug('Waiting for %0.3f second(s)...', wait_secs)
    time.sleep(wait_secs)

# Helper method to update the test suite result code
def test_suite_update_result(err_code):
    global test_suite_result_code

    if err_code > test_case_result_code:
        test_suite_result_code = err_code

# Helper method to update the test case result code and string
def test_case_update_result(err_code, err_str):
    global test_case_result_code
    global test_case_result_str

    if err_code > test_case_result_code:
        test_case_result_code = err_code
        test_case_result_str = err_str

# Helper method to get the test result string
def test_get_result_str(err_code):
    # Test result codes
    if (err_code == TEST_RESULT_PASS):
        test_res = 'Pass'
    elif (err_code == TEST_RESULT_WARNING):
        test_res = 'Warning'
    elif (err_code == TEST_RESULT_NOTICE):
        test_res = 'Notice'
    elif (err_code == TEST_RESULT_SKIP):
        test_res = 'Skip'
    elif (err_code == TEST_RESULT_ERROR):
        test_res = 'Error'
    elif (err_code == TEST_RESULT_CRITICAL):
        test_res = 'Critical'
    elif (err_code == TEST_RESULT_FATAL):
        test_res = 'Fatal'
    else:
        err_code = TEST_RESULT_ERROR
        err_str = 'Unknown error code ({0}) for the testing!'.format(err_code)
        test_logger.error('%s', err_str)
        raise TestFailureException(err_code, err_str)

    # Return with test result string
    return test_res

# Helper method to check the accessibility of the test suite report file
def test_check_report_file_access(file_data):
    sys_cmd = 'echo {0} > {1}'.format(shlex.quote(file_data), TEST_SUITE_REPORT_FILE)
    report_proc = subprocess.run(sys_cmd, shell=True)
    if report_proc.returncode:
        err_code = TEST_RESULT_ERROR
        err_str = 'Failed to access the test suite report file ({0})!'.format(TEST_SUITE_REPORT_FILE)
        test_logger.error('%s', err_str)
        raise TestFailureException(err_code, err_str)

# Helper method to write data to the test suite report file
def test_write_report_file(file_data):
    sys_cmd = 'echo {0} >> {1}'.format(shlex.quote(file_data), TEST_SUITE_REPORT_FILE)
    report_proc = subprocess.run(sys_cmd, shell=True)
    if report_proc.returncode:
        err_code = TEST_RESULT_ERROR
        err_str = 'Failed to write to the test suite report file ({0})!'.format(TEST_SUITE_REPORT_FILE)
        test_logger.error('%s', err_str)
        raise TestFailureException(err_code, err_str)

