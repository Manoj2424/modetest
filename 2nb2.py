import subprocess
import time
import os 
import signal


s1 = 'Connectors:'
s2 = 'CRTCs:'
s3 = 'Planes:'
s4 = 'formats:'
formats=[]


def getpara(string1):   
	output = subprocess.check_output("cat modetest | grep -A 2 " + string1, shell=True)
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
	output = subprocess.check_output("cat modetest | grep -m 1 " + string1, shell=True)
	temp = output.decode("utf-8")
	formats=temp.split()
	formats.pop(0)
	print(formats)


def validate(cmd):
	print(cmd)
	time.sleep(1)

	
conn_id = getpara(s1)	


crtc_id = getpara(s2)


plane_id = getpara(s3)


getformat(s4)


while (1):
	test_case = input("choice:")
	test_case=int(test_case)
	if test_case == 1:	
		for i in formats:
			cmd = "modetest -M NB2 -s " + conn_id + "@" + crtc_id + ":640x480@" + i
			validate(cmd)

	elif test_case == 2:
		for i in formats:
			cmd = "modetest -M NB2 -s " + conn_id + "@" + crtc_id + ":640x480@" + i + " -P " + plane_id+ "@" + crtc_id + ":200x200+30+30"
			validate(cmd)

	elif test_case == 3:
		for i in formats:
			cmd = "modetest -M NB2 -s " + conn_id + "@" + crtc_id + ":640x480@" + i + " -P " + plane_id+ "@" + crtc_id + ":200x200+30+30" +" -C"
			validate(cmd)

	elif test_case == 4:
		for i in formats:
			cmd = "modetest -M NB2 -s " + conn_id + "@" + crtc_id + ":640x480@" + i + " -P " + plane_id+ "@" + crtc_id + ":200x200+30+30" +" -v"
			validate(cmd)	

	elif test_case == 5:
		for i in formats:
			cmd = "modetest -M NB2 -s " + conn_id + "@" + crtc_id + ":640x480@" + i + " -P " + plane_id+ "@" + crtc_id + ":200x200+30+30" +" -C " + "-v"
			validate(cmd)
	else:
		print("Null")				  	




