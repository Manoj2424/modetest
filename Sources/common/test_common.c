/****************************************************************
 * File Name: test_common.c                                     *
 * Author: Ganesh Shanubhogue                                   *
 * Last Modified: 10-Feb-2020                                   *
 *                                                              *
 * Copyright: (c) 2019 ExaLeap Semiconductors.                  *
 * ExaLeap Proprietary and Confidential. All rights reserved.   *
 ***************************************************************/

/* Includes */
#include <test_common.h>

/* Global variables */
test_result_t test_result;
char test_result_msg[TEST_RESULT_MSG_LEN];
char test_sys_host_name[TEST_SYS_HOST_NAME_LEN];
int test_rand_seed = 0;

/* Function to get the host system IP address */
char *test_get_sys_inet_addr(void)
{
    int retval = TEST_RESULT_PASS;
    struct sockaddr_in target_addr;
    struct sockaddr_in local_addr;
    int server_socket;
    socklen_t socket_len;
    static char test_sys_inet_addr[INET_ADDRSTRLEN];

    /* Clear the socket details */
    memset(&target_addr, 0, sizeof(target_addr));
    memset(&local_addr, 0, sizeof(local_addr));

    /* Create the socket */
    server_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (server_socket == TEST_INVALID_SOCKET_NUM) {
        PRINT_ERR("Failed to create the server socket!\n");
        return NULL;
    }

    /* Connect to test DNS server */
    target_addr.sin_family = AF_INET;
    target_addr.sin_port = htons(TEST_SAMPLE_DNS_SERVER_PORT);
    target_addr.sin_addr.s_addr = inet_addr(TEST_SAMPLE_DNS_SERVER_IP);
    retval = connect(server_socket, (struct sockaddr *)&target_addr, sizeof(target_addr));
    if (retval != TEST_RESULT_PASS) {
        PRINT_ERR("Failed to connect to the test DNS server!\n");
        return NULL;
    }

    /* Get local socket info */
    socket_len = sizeof(local_addr);
    retval = getsockname(server_socket, (struct sockaddr *)&local_addr, &socket_len);
    if (retval != TEST_RESULT_PASS) {
        PRINT_ERR("Failed to get the local socket info!\n");
        return NULL;
    }
    inet_ntop(local_addr.sin_family, &(local_addr.sin_addr), test_sys_inet_addr, sizeof(test_sys_inet_addr));

    /* Close the server socket */
    close(server_socket);

    return test_sys_inet_addr;
}

/* Function to get the name with IP address of host system */
char *test_get_sys_name(void)
{
    int retval = TEST_RESULT_PASS;
    int host_name_len;

    /* Clear the host name details */
    memset(test_sys_host_name, 0, sizeof(test_sys_host_name));

    /* Get the System host name */
    retval = gethostname(test_sys_host_name, TEST_SYS_HOST_NAME_LEN);
    if (retval != TEST_RESULT_PASS) {
        snprintf(test_sys_host_name, TEST_SYS_HOST_NAME_LEN, "Unknown");
    }

    /* Append the IP address */
    host_name_len = strlen(test_sys_host_name);
    snprintf((test_sys_host_name + host_name_len), (TEST_SYS_HOST_NAME_LEN - host_name_len), " (%s)", test_get_sys_inet_addr());

    return test_sys_host_name;
}

/* Function to get the timestamp string */
char* test_get_formatted_time(char *fmt)
{
    static char time_str[32] = "";
    time_t rawtime;
    struct tm *timeinfo;

    time(&rawtime);
    timeinfo = localtime(&rawtime);

    strftime(time_str, sizeof(time_str), fmt, timeinfo);
    return time_str;
}

/* Function to convert the string to all lower case */
char *test_str_to_lower(char *str)
{
  unsigned char *p = (unsigned char *) str;

  while (*p) {
     *p = tolower((unsigned char) *p);
      p++;
  }

  return str;
}

/* Function to shuffle the elements of the array */
void test_array_shuffle(void *array, int n, int size)
{
    char tmp[size];
    char *arr = array;
    int stride = (size * sizeof(char));
    int random;
    int i;
    int j;

    if (n > 1) {
        for (i = 0; i < (n - 1); ++i) {
            random = rand();
            j = i + (random / ((RAND_MAX / (n - i)) + 1));

            memcpy(tmp, (arr + (j * stride)), size);
            memcpy((arr + (j * stride)), (arr + (i * stride)), size);
            memcpy((arr + (i * stride)), tmp, size);
        }
    }
}

/* Function to get the random number within the range:                                      *
 *  - Largest value rand() function can return depends on the RAND_MAX integer constant     *
 *    defined in the C Library. In GNU C Library, it is 2147483647 (0x7fffffff), which is   *
 *    the largest signed integer representable in 32 bits. In other libraries, it may be    *
 *    as low as 32767 (0x7fff).                                                             *
 *  - For Linux Systems using GNU C Library, this value is 2147483647 (0x7fffffff). Hence   *
 *    the maximum value of the random number that is possible with this function is limited *
 *    to (RAND_MAX - 1), i.e., 2147483646 (0x7ffffffe).                                     */
int test_get_random_number(int min, int max)
{
    int random;
    const int range = (max - min + 1);
    const int buckets = (RAND_MAX / range);
    const int limit = (buckets * range);

    do {
        random = rand();
    } while (random >= limit);

    return (min + (random / buckets));
}

/* Function to get the 64-bit random number */
unsigned long long int test_get_64bit_random_number(void)
{
    unsigned long long int random;

    random = (unsigned int)test_get_random_number(0x0, ALL_BIT_SET_16BIT);
    random = ((random << 16) | (unsigned int)test_get_random_number(0x0, ALL_BIT_SET_16BIT));
    random = ((random << 16) | (unsigned int)test_get_random_number(0x0, ALL_BIT_SET_16BIT));
    random = ((random << 16) | (unsigned int)test_get_random_number(0x0, ALL_BIT_SET_16BIT));

    return random;
}

/* Function to get the huge random number within the range */
unsigned long long int test_get_huge_random_number(unsigned long long int min, unsigned long long int max)
{
    unsigned long long int random;
    const unsigned long long int range = (max - min + 1);
    const unsigned long long int buckets = (ALL_BIT_SET_64BIT / range);
    const unsigned long long int limit = (buckets * range);

    do {
        random = test_get_64bit_random_number();
    } while (random >= limit);

    return (min + (random / buckets));
}

/* Function to get the random number array with unique values for specified length */
int test_get_unique_random_num_array(int *rand_array, int size, int min, int max)
{
    int i;
    int *array;
    int range;
    int array_size;
    int retval = TEST_RESULT_PASS;

    /* Check the input parameters */
    if (max < min) {
        ERROR_TEST("Invalid range (min: %d, max: %d) to generate the unique random number array!", min, max);
    }
    range = (max - min + 1);
    if ((size <= 0) || (size > range)) {
        ERROR_TEST("Invalid random array size %d (min: %d, max %d) to generate the unique random number array!", size, min, max);
    }

    /* Allocate memory for the linear array */
    array_size = (range * sizeof(array[0]));
    array = malloc(array_size);
    if (array == NULL) {
        ERROR_TEST("Failed to allocate the memory for the linear array of size %d bytes!", array_size);
    }

    /* Fill the array with linear numbers from min to max and shuffle */
    for (i = 0; i < range; i++) array[i] = (min + i);
    test_array_shuffle(array, range, sizeof(array[0]));

    /* Fill the random array with required size */
    for (i = 0; i < size; i++) rand_array[i] = array[i];

    /* Free allocated memory and return */
    free(array);
    return retval;
}

/* Function to sort the array */
int test_sort_array(int *array, int size)
{
    int i;
    int j;
    int tmp;

    for (i = 1; i < size; i++) {
        for (j = 0; j < (size - i); j++) {
            if (array[j] > array[j + 1]) {
                tmp = array[j];
                array[j] = array[j + 1];
                array[j + 1] = tmp;
            }
        }
    }

    return 0;
}

/* Function to uniquely sort the array (deleting duplicates) */
int test_sort_array_unique(int *array, int *size)
{
    int i;
    int j;
    int k;

    /* Sort the array before checking for duplicates */
    test_sort_array(array, *size);

    /* Check for duplicates */
    for (i = 1; i < *size; i++) {
        if (array[i] == array[i - 1]) {
            for (j = i; array[j] == array[i - 1] && j <= *size; j++, (*size)--);
            for (k = 0; k < (*size - i); k++) {
                array[i + k] = array[j + k];
            }
        }
    }

    return 0;
}

/* Function to get the random number within the range excluding the values from exclude list */
int test_get_random_number_excluded(int min, int max, int *exc_array, int exc_size)
{
    int random;
    int i;

    /* Sort uniquely the exclusion array (removing any duplicates) */
    test_sort_array_unique(exc_array, &exc_size);

    /* Get the random number in the range and adjust it based on the exclude list */
    random = test_get_random_number(min, (max - exc_size));
    for (i = 0; i < exc_size; i++) {
        if (random >= exc_array[i]) {
            random++;
        } else {
            break;
        }
    }

    return random;
}

