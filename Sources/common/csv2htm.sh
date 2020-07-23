#!/bin/bash


#####################################################################
# File Name: csv2htm.sh                                             #
# Author: Ganesh Shanubhogue                                        #
# Last Modified: 02-Apr-2020                                        #
#                                                                   #
# Copyright: (c) 2020 ExaLeap Semiconductors.                       #
# ExaLeap Proprietary and Confidential. All rights reserved.        #
#####################################################################

# Helper script to conver the test suite report file to HTML
# Usage:
#  ./csv2htm.sh <test_repot_file> <ip_namea> <log_file>

# Verify the input parameters for script
test_report_file=$1
test_ip_name=${2^^}
test_log_file=$3
if [ -z $1 ] || [ -z $2 ] || [ -z $3 ]; then
	echo "TEST_ERROR: Invalid arguments for converting report file to HTML!"
	echo "Usage:"
	echo "  $0 report_file ip_name log_file"
	exit
fi

# Check for the availability of report file
if [ ! -f "${test_report_file}" ]; then
	echo "TEST_ERROR: Test suite report file (${test_report_file}) for ${test_ip_name} doesn't exists!"
	exit
fi

# Check for the availability of log file
if [ ! -f "${test_log_file}" ]; then
	echo "TEST_ERROR: Test suite log file (${test_log_file}) for ${test_ip_name} doesn't exists!"
	exit
fi

# Variables used within the script
test_report_csv=.test_report.csv
test_log_output=.test_log_output
report_header=$(head -n 1 $test_report_file)
tail -n $(expr $(cat $test_report_file | wc -l) - 1) $test_report_file > $test_report_csv
total_tests=$(expr $(cat $test_report_csv | wc -l) - 1)
total_passed=$(cut -d "," -f3 $test_report_csv | grep -i "Pass" | wc -l)
total_warning=$(cut -d "," -f3 $test_report_csv | grep -i "Warning" | wc -l)
total_notice=$(cut -d "," -f3 $test_report_csv | grep -i "Notice" | wc -l)
total_skip=$(cut -d "," -f3 $test_report_csv | grep -i "Skip" | wc -l)
total_error=$(cut -d "," -f3 $test_report_csv | grep -i "Error" | wc -l)
total_critical=$(cut -d "," -f3 $test_report_csv | grep -i "Critical" | wc -l)
total_fatal=$(cut -d "," -f3 $test_report_csv | grep -i "Fatal" | wc -l)
total_failed=$(expr $total_warning + $total_notice + $total_skip + $total_error + $total_critical + $total_fatal)

# Strip the color codes in the log to display in the HTML
sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g" $test_log_file > $test_log_output

awk -v test_ip_name="$test_ip_name" -v report_header="$report_header" -v total_tests="$total_tests" -v total_passed="$total_passed" -v total_warning="$total_warning" -v total_notice="$total_notice" -v total_skip="$total_skip" -v total_error="$total_error" -v total_critical="$total_critical" -v total_fatal="$total_fatal" -v total_failed="$total_failed" -v test_log_file="$test_log_file" -v test_log_output="$test_log_output" -F, '
BEGIN {
  print "<html><body></br></br><td><b><font face=\"verdana\" size=5>"report_header"</font></b></td></br></br></br>"
  print "<table border=1 cellspacing=1 cellpadding=4>"
}

NR==1 {
  # Header row
  print "<tr align=\"center\">"

  for ( i = 1; i <= NF; i++ ) {
    print "<td><b><font face=\"verdana\" size=3>"$i"</font></b></td>"
  }
  print "</tr>"
}

NR>1 {
  # Data rows
  print "<tr align=\"justify\">"
  color="red"
  if( $4 == 0 ) {
	# Pass
    color="green"
  }
  if( $4 == 1 ) {
	# Warning
    color="magenta"
  }
  if( $4 == 2 ) {
	# Notice
    color="purple"
  }
  if( $4 == 3 ) {
	# Skip
    color="blue"
  }
  for ( i = 1; i <= NF; i++ ) {
      print "<td><font color=\""color"\" face=\"verdana\" size=2>"$i"</font></td>"
  }
  print "</tr>"
}
END {
  print "</table>"
  print "<html><body></br></br></br><td><b><font face=\"verdana\" size=4>"test_ip_name" Test Summary:</font></b></td></br></br>"
  print "<table border=1 cellspacing=1 cellpadding=4>"
  print "<tr align=\"justify\"><td><b><font color=\"black\" face=\"verdana\" size=3>Total Tests:</font></b></td>"
  print "<td><b><font color=\"black\" face=\"verdana\" size=3>"total_tests"\n</font></b></td></tr>"
  print "<tr align=\"justify\"><td><b><font color=\"green\" face=\"verdana\" size=3>Total Passed:</font></b></td>"
  print "<td><b><font color=\"green\" face=\"verdana\" size=3>"total_passed"\n</font></b></td></tr>"
  print "<tr align=\"justify\"><td><b><font color=\"red\" face=\"verdana\" size=3>Total Failed:</font></b></td>"
  print "<td><b><font color=\"red\" face=\"verdana\" size=3>"total_failed"\n</font></b></td></tr>"
  print "<tr align=\"justify\"><td><b><font color=\"magenta\" face=\"verdana\" size=3>&nbsp;&nbsp;Total Warning:</font></b></td>"
  print "<td><b><font color=\"magenta\" face=\"verdana\" size=3>"total_warning"\n</font></b></td></tr>"
  print "<tr align=\"justify\"><td><b><font color=\"purple\" face=\"verdana\" size=3>&nbsp;&nbsp;Total Notice:</font></b></td>"
  print "<td><b><font color=\"purple\" face=\"verdana\" size=3>"total_notice"\n</font></b></td></tr>"
  print "<tr align=\"justify\"><td><b><font color=\"blue\" face=\"verdana\" size=3>&nbsp;&nbsp;Total Skip:</font></b></td>"
  print "<td><b><font color=\"blue\" face=\"verdana\" size=3>"total_skip"\n</font></b></td></tr>"
  print "<tr align=\"justify\"><td><b><font color=\"red\" face=\"verdana\" size=3>&nbsp;&nbsp;Total Error:</font></b></td>"
  print "<td><b><font color=\"red\" face=\"verdana\" size=3>"total_error"\n</font></b></td></tr>"
  print "<tr align=\"justify\"><td><b><font color=\"red\" face=\"verdana\" size=3>&nbsp;&nbsp;Total Critical:</font></b></td>"
  print "<td><b><font color=\"red\" face=\"verdana\" size=3>"total_critical"\n</font></b></td></tr>"
  print "<tr align=\"justify\"><td><b><font color=\"red\" face=\"verdana\" size=3>&nbsp;&nbsp;Total Fatal:</font></b></td>"
  print "<td><b><font color=\"red\" face=\"verdana\" size=3>"total_fatal"\n</font></b></td></tr>"
  print "</table>"
  print "</br></br><td><b><font face=\"verdana\" size=3>"test_ip_name" test suite log location:</b> "test_log_file" (click <a href="test_log_output">here</a> to open)</font></td></br></br>"
  print "</body></html>"
}
' $test_report_csv

