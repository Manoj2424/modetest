/****************************************************************
 * File Name: test_common.h                                     *
 * Author: Ganesh Shanubhogue                                   *
 * Last Modified: 10-Feb-2020                                   *
 *                                                              *
 * Copyright: (c) 2019 ExaLeap Semiconductors.                  *
 * ExaLeap Proprietary and Confidential. All rights reserved.   *
 ***************************************************************/

#ifndef __TEST_COMMON_H__
#define __TEST_COMMON_H__

/* Includes */
#include <stdbool.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <pthread.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <stdarg.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <time.h>
#include <errno.h>
#include <stdint.h>
#include <inttypes.h>

/* Common defines */
#define TEST_TIME_FORMAT                "%Y%m%d_%H%M%S"
#define TEST_SYS_HOST_NAME_LEN          128
#define TEST_SAMPLE_DNS_SERVER_IP       "8.8.8.8"
#define TEST_SAMPLE_DNS_SERVER_PORT     4567
#define TEST_INVALID_SOCKET_NUM         (-1)
#define TEST_INVALID_FILE_DESC          (-1)
#define TEST_ASCII_PRINTABLE_MIN        0x20
#define TEST_ASCII_PRINTABLE_MAX        0x7e

/* Test results reporting */
#define TEST_RESULT_MSG_LEN             512
#define TEST_RESULT_FILE                ".test_case_report"

/* Bit defines */
#define ALL_BIT_SET_64BIT               0xffffffffffffffff
#define ALL_BIT_SET_48BIT               0xffffffffffff
#define ALL_BIT_SET_32BIT               0xffffffff
#define ALL_BIT_SET_26BIT               0x3ffffff
#define ALL_BIT_SET_16BIT               0xffff
#define ALL_BIT_SET_8BIT                0xff
#define TOTAL_BITS_8BIT                 8
#define TOTAL_BITS_16BIT                16
#define TOTAL_BITS_26BIT                26
#define TOTAL_BITS_32BIT                32
#define TOTAL_BITS_48BIT                48
#define TOTAL_BITS_64BIT                64
#define TOTAL_BYTES_8BIT                1
#define TOTAL_BYTES_16BIT               2
#define TOTAL_BYTES_32BIT               4
#define TOTAL_BYTES_48BIT               6
#define TOTAL_BYTES_64BIT               8
#define BIT_MASK_16BIT_UPPER_8BIT       0xff00
#define BIT_MASK_16BIT_LOWER_8BIT       0x00ff
#define BIT_MASK_32BIT_UPPER_16BIT      0xffff0000
#define BIT_MASK_32BIT_LOWER_16BIT      0x0000ffff

/* Test result codes */
typedef enum test_result_tag {
    TEST_RESULT_PASS            = 0,            /* Test case is successful in all means */
    TEST_RESULT_WARNING         = 1,            /* Warning (not a failure), requires attention */
    TEST_RESULT_NOTICE          = 2,            /* Minor failure (test continues), but treated as failure */
    TEST_RESULT_SKIP            = 3,            /* Test skipped to execute, because of unimplemented/unsupported feature/scenario */
    TEST_RESULT_ERROR           = 4,            /* Test program error (not a IP failure), test code required to handle this scenario */
    TEST_RESULT_CRITICAL        = 5,            /* Critical failure (test stops), treated as failure (other tests can continue on IP) */
    TEST_RESULT_FATAL           = 6,            /* Fatal failure (test abandons), other tests can't continue on IP */
} test_result_t;

/* Global variables */
extern test_result_t test_result;
extern char test_result_msg[TEST_RESULT_MSG_LEN];
extern char test_sys_host_name[TEST_SYS_HOST_NAME_LEN];
extern int test_rand_seed;

/* Macro to check if the test can continue */
#define TEST_CHECK_CONTINUE(res)        ((((res) == TEST_RESULT_PASS) || ((res) == TEST_RESULT_WARNING) || ((res) == TEST_RESULT_NOTICE)) ? true : false)

/* Macro to get the bit values of registers */
#define TEST_GET_REG_BIT_VAL(val, pos, mask)    (((unsigned int)(val) >> pos) & mask)

/* Macro to set the bit values of registers */
#define TEST_SET_REG_BIT_VAL(val, pos, mask)    (((unsigned int)(val) & mask) << pos)

/* Macro to check if the given number is even or odd */
#define TEST_NUM_IS_EVEN(x)             ((x % 2) == 0 ? true : false)
#define TEST_NUM_IS_ODD(x)              ((x % 2) == 1 ? true : false)

/* Macro to check if the parameters are within the allowable range */
#define TEST_PARAM_RANGE_IS_ALLOWABLE(param1, param2, range)    ((((param1 - range) <= param2) && ((param1 + range) >= param2)) ? true : false)

/* Macro to get enable/disable string */
#define TEST_GET_EN_DIS_STR(x)          ((x) == false ? "Disable" : "Enable")

/* Macro to get boolean string */
#define TEST_GET_BOOL_STR(x)            ((x) == false ? "False" : "True")

/* Macro to get high/low string */
#define TEST_GET_HIGH_LOW_STR(x)        ((x) == false ? "Low" : "High")

/* Macro to get yes/no string */
#define TEST_GET_YESNO_STR(x)           ((x) == false ? "No" : "Yes")

/* Macro to get up/down string */
#define TEST_GET_UPDOWN_STR(x)          ((x) == false ? "Down" : "Up")

/* Debug print options */
#undef DBG_PRINT_TIMESTAMP
#define DBG_PRINT_TERM_COLOR
#define TEST_PRINT_DBG_SETUP
#define TEST_PRINT_MSG_LEN              1024

/* Terminal color codes */
#ifdef DBG_PRINT_TERM_COLOR
#define KNRM  "\x1B[0m"
#define KRED  "\x1B[31m"
#define KGRN  "\x1B[32m"
#define KYEL  "\x1B[33m"
#define KBLU  "\x1B[34m"
#define KMAG  "\x1B[35m"
#define KCYN  "\x1B[36m"
#define KWHT  "\x1B[37m"
#else
#define KNRM  ""
#define KRED  ""
#define KGRN  ""
#define KYEL  ""
#define KBLU  ""
#define KMAG  ""
#define KCYN  ""
#define KWHT  ""
#endif /* DBG_PRINT_TERM_COLOR */

/* Debug print utilities */
#ifdef DBG_PRINT_TIMESTAMP
#define DBG_TIMESTAMP_STR   test_get_formatted_time("%Y-%m-%d %H:%M:%S ")
#else
#define DBG_TIMESTAMP_STR   ""
#endif /* DBG_PRINT_TIMESTAMP */

/* Macros to print messages */
#define PRINT_MSG(fmt, args...)     fprintf(stdout, fmt, ##args)
#define PRINT_INFO(fmt, args...)    fprintf(stdout, "%s:%d:%s(): " fmt, __FILE__, __LINE__, __func__, ##args)
#define PRINT_DBG(fmt, args...)     fprintf(stdout, "%sTEST_DEBUG: %s:%d:%s(): " fmt, DBG_TIMESTAMP_STR, __FILE__, __LINE__, __func__, ##args)
#define PRINT_WARN(fmt, args...)    fprintf(stdout, KCYN "TEST_WARNING: %s:%d:%s(): " fmt KNRM, __FILE__, __LINE__, __func__, ##args)
#define PRINT_ERR(fmt, args...)     fprintf(stdout, KCYN "TEST_ERROR: %s:%d:%s(): " fmt KNRM, __FILE__, __LINE__, __func__, ##args)
#define PRINT_FAIL(fmt, args...)    fprintf(stdout, KRED "TEST_FAIL: %s:%d:%s(): " fmt KNRM, __FILE__, __LINE__, __func__, ##args)
#define PRINT_REPORT(fmt, args...)                                                                          \
    do {                                                                                                    \
        PRINT_DBG("--------------------------------------------------------------------------------\n");    \
        PRINT_DBG(fmt, ##args);                                                                             \
        PRINT_DBG("--------------------------------------------------------------------------------\n");    \
    } while(0)
#define PRINT_BANNER(fmt, args...)                                                                          \
    do {                                                                                                    \
        PRINT_DBG("================================================================================\n");    \
        PRINT_DBG(fmt, ##args);                                                                             \
        PRINT_DBG("================================================================================\n");    \
    } while(0)
#define PRINT_FAILED(fmt, args...)  PRINT_BANNER(KRED "TEST_FAILED: " fmt KNRM, ##args)
#define PRINT_PASSED(fmt, args...)  PRINT_BANNER(KGRN "TEST_PASSED: " fmt KNRM, ##args)
#define PRINT_PASS(fmt, args...)    PRINT_REPORT(KGRN "TEST_PASS: " fmt KNRM, ##args)
#define PRINT_LOG(fname, mode, fmt, args...)                                            \
    do {                                                                                \
        FILE *_fp = fopen(fname, mode);                                                 \
        if (_fp == NULL) PRINT_ERR("Failed to open the log file (%s)!", fname);         \
        fprintf(_fp, fmt, ##args);                                                      \
        fclose(_fp);                                                                    \
    } while(0)

#define TEST_DEBUG_LEVEL 3
#ifdef TEST_DEBUG_LEVEL
#if (TEST_DEBUG_LEVEL > 0)
#define PRINT_DBG1(fmt, args...)                                            \
    fprintf(stdout, "%sTEST_DEBUG1: %s:%d:%s(): " fmt, DBG_TIMESTAMP_STR,   \
        __FILE__, __LINE__, __func__, ##args)
#else
#define PRINT_DBG1(fmt, args...)
#endif
#if (TEST_DEBUG_LEVEL > 1)
#define PRINT_DBG2(fmt, args...)                                            \
    fprintf(stdout, "%sTEST_DEBUG2: %s:%d:%s(): " fmt, DBG_TIMESTAMP_STR,   \
        __FILE__, __LINE__, __func__, ##args)
#else
#define PRINT_DBG2(fmt, args...)
#endif
#if (TEST_DEBUG_LEVEL > 2)
#define PRINT_DBG3(fmt, args...)                                            \
    fprintf(stdout, "%sTEST_DEBUG3: %s:%d:%s(): " fmt, DBG_TIMESTAMP_STR,   \
        __FILE__, __LINE__, __func__, ##args)
#else
#define PRINT_DBG3(fmt, args...)
#endif
#else
#define PRINT_DBG1(fmt, args...)
#define PRINT_DBG2(fmt, args...)
#define PRINT_DBG3(fmt, args...)
#endif /* TEST_DEBUG_LEVEL */

/* Macros to check test status */
#define ASSERT_TRUE(val, fmt, args...)                                          \
    do {                                                                        \
        if (!val) {                                                             \
            fprintf(stdout, KRED "TEST_CRITICAL: %s:%d:%s(): " fmt "\n" KNRM,   \
                __FILE__, __LINE__, __func__, ##args);                          \
            fprintf(stdout, KRED "  Expected: True\n" KNRM);                    \
            fprintf(stdout, KRED "  Actual:   False\n" KNRM);                   \
            snprintf(test_result_msg, TEST_RESULT_MSG_LEN, fmt, ##args);        \
            PRINT_LOG(TEST_RESULT_FILE, "w+", "%s", test_result_msg);           \
            test_result = TEST_RESULT_CRITICAL;                                 \
            return test_result;                                                 \
        }                                                                       \
    } while(0)

#define ASSERT_FALSE(val, fmt, args...)                                         \
    do {                                                                        \
        if (val) {                                                              \
            fprintf(stdout, KRED "TEST_CRITICAL: %s:%d:%s(): " fmt "\n" KNRM,   \
                __FILE__, __LINE__, __func__, ##args);                          \
            fprintf(stdout, KRED "  Expected: False\n" KNRM);                   \
            fprintf(stdout, KRED "  Actual:   True\n" KNRM);                    \
            snprintf(test_result_msg, TEST_RESULT_MSG_LEN, fmt, ##args);        \
            PRINT_LOG(TEST_RESULT_FILE, "w+", "%s", test_result_msg);           \
            test_result = TEST_RESULT_CRITICAL;                                 \
            return test_result;                                                 \
        }                                                                       \
    } while(0)

#define ASSERT_EQUAL(exp, act, fmt, args...)                                    \
    do {                                                                        \
        if (exp != act) {                                                       \
            fprintf(stdout, KRED "TEST_CRITICAL: %s:%d:%s(): " fmt "\n" KNRM,   \
                __FILE__, __LINE__, __func__, ##args);                          \
            fprintf(stdout, KRED "  Expected: %d (0x%x)\n" KNRM, exp, exp);     \
            fprintf(stdout, KRED "  Actual:   %d (0x%x)\n" KNRM, act, act);     \
            snprintf(test_result_msg, TEST_RESULT_MSG_LEN, fmt, ##args);        \
            PRINT_LOG(TEST_RESULT_FILE, "w+", "%s", test_result_msg);           \
            test_result = TEST_RESULT_CRITICAL;                                 \
            return test_result;                                                 \
        }                                                                       \
    } while(0)

#define ASSERT_NOT_EQUAL(exp, act, fmt, args...)                                \
    do {                                                                        \
        if (exp == act) {                                                       \
            fprintf(stdout, KRED "TEST_CRITICAL: %s:%d:%s(): " fmt "\n" KNRM,   \
                __FILE__, __LINE__, __func__, ##args);                          \
            fprintf(stdout, KRED "  Expected: != %d (0x%x)\n" KNRM, exp, exp);  \
            fprintf(stdout, KRED "  Actual:   %d (0x%x)\n" KNRM, act, act);     \
            snprintf(test_result_msg, TEST_RESULT_MSG_LEN, fmt, ##args);        \
            PRINT_LOG(TEST_RESULT_FILE, "w+", "%s", test_result_msg);           \
            test_result = TEST_RESULT_CRITICAL;                                 \
            return test_result;                                                 \
        }                                                                       \
    } while(0)

#define ASSERT_SUCCESS(val)                                                     \
    do {                                                                        \
        int _rc = val;                                                          \
        if (!TEST_CHECK_CONTINUE(_rc)) {                                        \
            fprintf(stdout, KRED "TEST_ASSERTION: %s:%d:%s(): "                 \
                "Test returned due to previous failures!\n" KNRM,               \
                __FILE__, __LINE__, __func__);                                  \
            return _rc;                                                         \
        }                                                                       \
    } while(0)

#define FLUNK_TEST(fmt, args...)                                                \
    do {                                                                        \
        fprintf(stdout, KRED "TEST_FATAL: %s:%d:%s(): " fmt "\n" KNRM,          \
            __FILE__, __LINE__, __func__, ##args);                              \
        snprintf(test_result_msg, TEST_RESULT_MSG_LEN, fmt, ##args);            \
        PRINT_LOG(TEST_RESULT_FILE, "w+", "%s", test_result_msg);               \
        test_result = TEST_RESULT_FATAL;                                        \
        return test_result;                                                     \
    } while(0)

#define EXPECT_TRUE(val, fmt, args...)                                          \
    do {                                                                        \
        if (!val) {                                                             \
            fprintf(stdout, KMAG "TEST_NOTICE: %s:%d:%s(): " fmt "\n" KNRM,     \
                __FILE__, __LINE__, __func__, ##args);                          \
            fprintf(stdout, KMAG "  Expected: True\n" KNRM);                    \
            fprintf(stdout, KMAG "  Actual:   False\n" KNRM);                   \
            if (test_result < TEST_RESULT_NOTICE) {                             \
                snprintf(test_result_msg, TEST_RESULT_MSG_LEN, fmt, ##args);    \
                PRINT_LOG(TEST_RESULT_FILE, "w+", "%s", test_result_msg);       \
                test_result = TEST_RESULT_NOTICE;                               \
            }                                                                   \
            return test_result;                                                 \
        }                                                                       \
    } while(0)

#define EXPECT_FALSE(val, fmt, args...)                                         \
    do {                                                                        \
        if (val) {                                                              \
            fprintf(stdout, KMAG "TEST_NOTICE: %s:%d:%s(): " fmt "\n" KNRM,     \
                __FILE__, __LINE__, __func__, ##args);                          \
            fprintf(stdout, KMAG "  Expected: False\n" KNRM);                   \
            fprintf(stdout, KMAG "  Actual:   True\n" KNRM);                    \
            if (test_result < TEST_RESULT_NOTICE) {                             \
                snprintf(test_result_msg, TEST_RESULT_MSG_LEN, fmt, ##args);    \
                PRINT_LOG(TEST_RESULT_FILE, "w+", "%s", test_result_msg);       \
                test_result = TEST_RESULT_NOTICE;                               \
            }                                                                   \
            return test_result;                                                 \
        }                                                                       \
    } while(0)

#define EXPECT_EQUAL(exp, act, fmt, args...)                                    \
    do {                                                                        \
        if (exp != act) {                                                       \
            fprintf(stdout, KMAG "TEST_NOTICE: %s:%d:%s(): " fmt "\n" KNRM,     \
                __FILE__, __LINE__, __func__, ##args);                          \
            fprintf(stdout, KMAG "  Expected: %d (0x%x)\n" KNRM, exp, exp);     \
            fprintf(stdout, KMAG "  Actual:   %d (0x%x)\n" KNRM, act, act);     \
            if (test_result < TEST_RESULT_NOTICE) {                             \
                snprintf(test_result_msg, TEST_RESULT_MSG_LEN, fmt, ##args);    \
                PRINT_LOG(TEST_RESULT_FILE, "w+", "%s", test_result_msg);       \
                test_result = TEST_RESULT_NOTICE;                               \
            }                                                                   \
            return test_result;                                                 \
        }                                                                       \
    } while(0)

#define EXPECT_NOT_EQUAL(exp, act, fmt, args...)                                \
    do {                                                                        \
        if (exp == act) {                                                       \
            fprintf(stdout, KMAG "TEST_NOTICE: %s:%d:%s(): " fmt "\n" KNRM,     \
                __FILE__, __LINE__, __func__, ##args);                          \
            fprintf(stdout, KMAG "  Expected: != %d (0x%x)\n" KNRM, exp, exp);  \
            fprintf(stdout, KMAG "  Actual:   %d (0x%x)\n" KNRM, act, act);     \
            if (test_result < TEST_RESULT_NOTICE) {                             \
                snprintf(test_result_msg, TEST_RESULT_MSG_LEN, fmt, ##args);    \
                PRINT_LOG(TEST_RESULT_FILE, "w+", "%s", test_result_msg);       \
                test_result = TEST_RESULT_NOTICE;                               \
            }                                                                   \
            return test_result;                                                 \
        }                                                                       \
    } while(0)

#define SKIP_TEST(fmt, args...)                                                 \
    do {                                                                        \
        fprintf(stdout, KBLU "TEST_SKIP: %s:%d:%s(): " fmt "\n" KNRM,           \
                __FILE__, __LINE__, __func__, ##args);                          \
        snprintf(test_result_msg, TEST_RESULT_MSG_LEN, fmt, ##args);            \
        PRINT_LOG(TEST_RESULT_FILE, "w+", "%s", test_result_msg);               \
        test_result = TEST_RESULT_SKIP;                                         \
        return test_result;                                                     \
    } while(0)

#define WARN_TEST(fmt, args...)                                                     \
    do {                                                                            \
        fprintf(stdout, KCYN "TEST_WARNING: %s:%d:%s(): " fmt "\n" KNRM,            \
                __FILE__, __LINE__, __func__, ##args);                              \
        if (test_result < TEST_RESULT_WARNING) {                                    \
            snprintf(test_result_msg, TEST_RESULT_MSG_LEN, fmt, ##args);            \
            PRINT_LOG(TEST_RESULT_FILE, "w+", "%s", test_result_msg);               \
            test_result = TEST_RESULT_WARNING;                                      \
        }                                                                           \
        return test_result;                                                         \
    } while(0)

#define ERROR_TEST(fmt, args...)                                                \
    do {                                                                        \
        fprintf(stdout, KRED "TEST_ERROR: %s:%d:%s(): " fmt "\n" KNRM,          \
                __FILE__, __LINE__, __func__, ##args);                          \
        snprintf(test_result_msg, TEST_RESULT_MSG_LEN, fmt, ##args);            \
        PRINT_LOG(TEST_RESULT_FILE, "w+", "%s", test_result_msg);               \
        test_result = TEST_RESULT_ERROR;                                        \
        return test_result;                                                     \
    } while(0)

/* Macro to swap two objects */
#define SWAP(x, y)                                                                  \
    do {                                                                            \
        unsigned char swap_temp[sizeof(x) == sizeof(y) ? (signed)sizeof(x) : -1];   \
        memcpy(swap_temp, &y, sizeof(x));                                           \
        memcpy(&y, &x, sizeof(x));                                                  \
        memcpy(&x, swap_temp, sizeof(x));                                           \
    } while(0)

/* Get number of elements of an array */
#define NUM_ARR_ELEMENTS(x) (sizeof(x) / sizeof(x[0]))

/* Macro to create print buffer from array */
#define TEST_ARR_LIST_SEP       ", "
#define ARRAY_TO_PRINT_BUFF(buf, arr, size, sep, fmt)               \
    do {                                                            \
        int _index;                                                 \
        char *_pos = buf;                                           \
        int _rem = sizeof(buf);                                     \
        int _len;                                                   \
        memset(buf, 0, _rem);                                       \
        for (_index = 0; _index < size; _index++) {                 \
            if (_index) {                                           \
                _len = snprintf(_pos, _rem, sep);                   \
                _pos += _len;                                       \
                _rem -= _len;                                       \
            }                                                       \
            _len = snprintf(_pos, _rem, fmt, arr[_index]);          \
            _pos += _len;                                           \
            _rem -= _len;                                           \
        }                                                           \
    } while(0)

/* Macro to search for a given element from array */
#define ARRAY_SEARCH_ELEMENT(element, pos, arr, size)               \
    do {                                                            \
        int _index;                                                 \
        bool _found = false;                                        \
        pos = -1;                                                   \
        for (_index = 0; _index < size; _index++) {                 \
            if (arr[_index] == element) {                           \
                _found = true;                                      \
                break;                                              \
            }                                                       \
        }                                                           \
        if (_found) pos = _index;                                   \
    } while(0)

/* Macro for the tests to wait in seconds */
#define TEST_WAIT_SECS(secs)                                            \
    do {                                                                \
        double _wait_secs = (double)secs;                               \
        PRINT_DBG3 ("Waiting for %0.3lf second(s)...\n", _wait_secs);   \
        test_wait_time += _wait_secs;                                   \
        usleep((unsigned int)(_wait_secs * 1000000));                   \
    } while(0)

/* Function declarations */
char *test_get_sys_inet_addr(void);
char *test_get_sys_name(void);
char* test_get_formatted_time(char *fmt);
char *test_str_to_lower(char *str);
void test_array_shuffle(void *array, int n, int size);
int test_get_random_number(int min, int max);
unsigned long long int test_get_64bit_random_number(void);
unsigned long long int test_get_huge_random_number(unsigned long long int min, unsigned long long int max);
int test_get_unique_random_num_array(int *rand_array, int size, int min, int max);
int test_sort_array(int *array, int size);
int test_sort_array_unique(int *array, int *size);
int test_get_random_number_excluded(int min, int max, int *exc_array, int exc_size);

#endif /* __TEST_COMMON_H__ */

