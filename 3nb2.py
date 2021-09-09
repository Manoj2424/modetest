import subprocess
import time
import os 
import signal
import random
import sys


s1 = 'Connectors:'
s2 = 'CRTCs:'
s3 = 'Planes:'
s4 = 'formats:'
formats=[]
plane_position_min=10
plane_position_max=60
plane_resolution_min=100
plane_resolution_max=400


def getpara(string1):   
	output = subprocess.check_output("cat modetest_u540 | grep -A 2 " + string1, shell=True)
	temp = output.decode("utf-8")
	table1=temp.split()
	for i in table1:
		a=i.isnumeric()
		if a==True:
			print(string1)
			print(i)
			return i


def getformat(string1):
	global formats
	print("Fetching Formats:") 
	output = subprocess.check_output("cat modetest_u540 | grep -m 1 " + string1, shell=True)
	temp = output.decode("utf-8")
	formats=temp.split()
	formats.pop(0)
	print(formats)


def random_number(minimum,maximum,step):
    return str(random.randrange(minimum,maximum,step))


def validate(cmd):
	print(cmd)
	time.sleep(1)

	
conn_id = getpara(s1)	


crtc_id = getpara(s2)


plane_id = getpara(s3)


getformat(s4)

test_case = sys.argv[1]
test_case=int(test_case)

if test_case == 1:	
	for i in formats:
		cmd = "modetest_u540 -M NB2 -s " + conn_id + "@" + crtc_id + ":640x480@" + i
		validate(cmd)

elif test_case == 2:
	for i in formats:
		plane_x_position=random_number(plane_position_min,plane_position_max,10)
		plane_y_position=random_number(plane_position_min,plane_position_max,10)
		plane_x_resolution=random_number(plane_resolution_min,plane_resolution_max,50)
		plane_y_resolution=random_number(plane_resolution_min,plane_resolution_max,50)

		cmd = "modetest -M NB2 -s " + conn_id + "@" + crtc_id + ":640x480@" + i + " -P " + plane_id+ "@" + crtc_id + ":" + plane_x_resolution + "x" + plane_y_resolution + "+" + plane_x_position + "+" + plane_y_position
		validate(cmd)

elif test_case == 3:
	for i in formats:
		plane_x_position=random_number(plane_position_min,plane_position_max,10)
		plane_y_position=random_number(plane_position_min,plane_position_max,10)
		plane_x_resolution=random_number(plane_resolution_min,plane_resolution_max,50)
		plane_y_resolution=random_number(plane_resolution_min,plane_resolution_max,50)

		cmd = "modetest -M NB2 -s " + conn_id + "@" + crtc_id + ":640x480@" + i + " -P " + plane_id+ "@" + crtc_id + ":" + plane_x_resolution + "x" + plane_y_resolution + "+" + plane_x_position + "+" + plane_y_position + " -C"
		validate(cmd)

elif test_case == 4:
	for i in formats:
		plane_x_position=random_number(plane_position_min,plane_position_max,10)
		plane_y_position=random_number(plane_position_min,plane_position_max,10)
		plane_x_resolution=random_number(plane_resolution_min,plane_resolution_max,50)
		plane_y_resolution=random_number(plane_resolution_min,plane_resolution_max,50)
		cmd = "modetest -M NB2 -s " + conn_id + "@" + crtc_id + ":640x480@" + i + " -P " + plane_id+ "@" + crtc_id + ":" + plane_x_resolution + "x" + plane_y_resolution + "+" + plane_x_position + "+" + plane_y_position +" -v"
		validate(cmd)	

elif test_case == 5:
	for i in formats:
		plane_x_position=random_number(plane_position_min,plane_position_max,10)
		plane_y_position=random_number(plane_position_min,plane_position_max,10)
		plane_x_resolution=random_number(plane_resolution_min,plane_resolution_max,50)
		plane_y_resolution=random_number(plane_resolution_min,plane_resolution_max,50)
		cmd = "modetest -M NB2 -s " + conn_id + "@" + crtc_id + ":640x480@" + i + " -P " + plane_id+ "@" + crtc_id + ":" + plane_x_resolution + "x" + plane_y_resolution + "+" + plane_x_position + "+" + plane_y_position + " -C " + "-v" 
		validate(cmd)
else:
	print("Null")				  	





