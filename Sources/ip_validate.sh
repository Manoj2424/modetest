#!/bin/bash

#####################################################################
# File Name: ip_validate.sh                                         #
# Author: Ganesh Shanubhogue                                        #
# Last Modified: 17-Feb-2020                                        #
#                                                                   #
# Copyright: (c) 2019 ExaLeap Semiconductors.                       #
# ExaLeap Proprietary and Confidential. All rights reserved.        #
#####################################################################

# Helper script to run the IP validation tests with following options:
#   1. Execute the IP validation tests for individual IPs by passing
#      required parameters specific to the IP.
#   2. Build IP test binaries for individual IP or for all supported IPs.
#   3. Install the IP validation package for individual IP or for all
#      suported IPs.

# Bash environment settings
set -o pipefail

# Bash terminal color codes
BNRM='\033[0m'
BRED='\033[31m'
BGRN='\033[32m'
BYEL='\033[33m'
BBLU='\033[34m'
BMAG='\033[35m'
BCYN='\033[36m'
BWHT='\033[37m'
BOLD=$(tput bold)
NORM=$(tput sgr0)

# Helper script error code
test_shell_success=0
test_shell_error=7

# Variables used within the script
time_string=$(date +%Y%m%d_%H%M%S)
time_print_str=$(date '+%A, %B %d, %Y %Z at %I:%M:%S %p')
copy_cmd='cp -a --no-preserve=mode,ownership'
test_working_dir=$(pwd)
test_log_dir=../logs
python_binary=python3

# Test input parameters
test_ip_type=
test_all_ips=false
test_found_ip=false
test_ip_params=
test_build_ip=false
test_install_ip=false

# Supported IPs types for the validation
declare -a ip_list=(
                     "uart"
                     "gpio"
                     "emmc"
                     "mmc_sdio"
                     "video"
                     "wdt"
                     "i2c"
                     "gpu"
                     "disp"
                     "rtc"
                     "usb_dev"
                     "usb_host"
                     "qspi"
                     "ethernet"
                     "adc"
                     "spi"
                     "audio"
                   )

# Function to print the error message and exit
test_error_exit() {
    echo -e "${BRED}ERROR: ${1}${BNRM}"
    exit ${test_shell_error}
}

# Function to print the usage
print_usage() {
    echo "Usage: $0 [options]"
    echo "  -n <ip_name>    Name of the IP to be tested. Specify one of the supported IP type for running"
    echo "                  the test. IP name can be specified as 'all' for the build and install option,"
    echo "                  but it is invalid for running the test."
    echo "  -o <test_opts>  Test options specific to the IP under test to be passed for running the test."
    echo "                  This option is applicable only for ruuning the test and not applicable for"
    echo "                  build and install."
    echo "  -b              Only build the binaries for specified IP or for all IPs (doesn't run test)."
    echo "  -i              Only install the IP validation package for specified IP or for all IPs"
    echo "                  (doesn't run test)."
    echo "  -h              Display this help information."
}

# Parse the command line arguments
while [ "$1" != "" ]; do
    case $1 in
        -n )
            shift
            test_ip_type=${1,,}
            ;;
        -o )
            shift
            test_ip_params=$1
            ;;
        -b )
            test_build_ip=true
            ;;
        -i )
            test_install_ip=true
            ;;
        -h )
            print_usage
            test_error_exit "Not a valid test argument ($1) to run the test!"
            ;;
        * )
            print_usage
            test_error_exit "Unknown option ($1) for the test!"
    esac
    shift
done

echo ":: Helper script to run the IP validation tests ::"
echo "Test run options:"
echo "  IP type:               ${test_ip_type^^}"
echo "  IP parameters:         ${test_ip_params^}"
echo "  Build IP binaries:     ${test_build_ip^}"
echo "  Install IP package:    ${test_install_ip^}"

# Check for IP type
if [ "${test_ip_type}" = 'all' ]; then
    test_all_ips=true
    if [ "${test_build_ip}" = false -a "${test_install_ip}" = false ]; then
        # Running IP validation tests not supported for all IPs at once
        test_error_exit "Running IP validation tests not supported for ALL IPs at once!"
    fi
elif [ ! -d "${test_ip_type}" ]; then
    # IP specific test files doesn't exists
    test_error_exit "Invalid IP type (${test_ip_type}) for the test (IP specific directory doesn't exists)!"
fi

# Build and install IP validation packages if requested
if [ "${test_all_ips}" = true ]; then
    for ip_type in "${ip_list[@]}"
    do
        if [ ! -d "${ip_type}" ]; then
            # IP specific test files doesn't exists
            echo "WARNING: IP specific directory for ${ip_type^^} doesn't exists, continuing with next IP..."
            continue
        else
            test_found_ip=true
        fi

        # Build the IP validation binaries if requested
        if [ "${test_build_ip}" = true ]; then
            echo "Building the IP validation binary for ${ip_type^^}..."
            ( cd ${ip_type} && make -f Makefile clean )
            ( cd ${ip_type} && make -f Makefile )
            retval=$?
            if [ ${retval} -ne 0 ]; then
                test_error_exit "Building the IP validation binary for ${ip_type^^} failed!"
            fi
        fi

        # Install the IP validation package if requested
        if [ "${test_install_ip}" = true ]; then
            echo "Installing the IP validation package for ${ip_type^^}..."
            ( cd ${ip_type} && make -f Makefile install )
            retval=$?
            if [ ${retval} -ne 0 ]; then
                test_error_exit "Installing the IP validation package for ${ip_type^^} failed!"
            fi
        fi
    done
    if [ "${test_found_ip}" = true ]; then
        echo "Successfully completed the operation for ALL available IPs"
        exit ${test_shell_success}
    else
        test_error_exit "None of the IP specific directories found to perform the operations!"
    fi
else
    # Build the IP validation binaries if requested
    if [ "${test_build_ip}" = true ]; then
        echo "Building the IP validation binary for ${test_ip_type^^}..."
        ( cd ${test_ip_type} && make -f Makefile clean )
        ( cd ${test_ip_type} && make -f Makefile )
        retval=$?
        if [ ${retval} -ne 0 ]; then
            test_error_exit "Building the IP validation binary for ${test_ip_type^^} failed!"
        fi
    fi

    # Install the IP validation package if requested
    if [ "${test_install_ip}" = true ]; then
        echo "Installing the IP validation package for ${test_ip_type^^}..."
        ( cd ${test_ip_type} && make -f Makefile install )
        retval=$?
        if [ ${retval} -ne 0 ]; then
            test_error_exit "Installing the IP validation package for ${test_ip_type^^} failed!"
        fi
    fi

    # Return if requested either of install or build
    if [ "${test_build_ip}" = true -o "${test_install_ip}" = true ]; then
        echo "Successfully completed the operations for ${test_ip_type^^}"
        exit ${test_shell_success}
    fi
fi

# Create the test log directory if doesn't exists
(cd ${test_ip_type} && mkdir -p ${test_log_dir} )

# Run the IP specific validation tests
echo ":: Starting the validation test for ${test_ip_type^^} ::"
test_python_file=test_${test_ip_type}.py
echo "Using the python file ${test_python_file} for ${test_ip_type^^} validation..."
test_log_file=${test_ip_type}_log_${time_string}.txt
echo "Using the log file ${test_log_file} for ${test_ip_type^^} validation..."
( cd ${test_ip_type} && ${python_binary} ${test_python_file} ${test_ip_params} |& tee -a ${test_log_dir}/${test_log_file} )
retval=$?
if [ ${retval} -ne 0 ]; then
    echo -e "${BRED}Test suite for ${test_ip_type^^} returned with error code ${retval}!${BNRM}"
    exit ${retval}
else
    echo -e "${BGRN}Test suite for ${test_ip_type^^} is successfull with return value ${retval}!${BNRM}"
    exit ${retval}
fi

