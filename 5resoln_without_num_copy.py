import subprocess
import time

resolution=[]
timing_parameters=[]


def find_resolution():
	temp=[]
	max_res=0
	global resolution
	output = subprocess.check_output("cat modetest | grep '\#'", shell=True)
	
	new = output.split()
	for x in new:
		if x.startswith(b'#'):
			temp.append(x)		
	temp = list(set(temp))
	max_res = len(temp)

	temp = output.decode("utf-8")
	#print(temp)
	temp = temp.splitlines()
	#print(temp)
	for i in range(max_res):
		line = temp[i]
		line = line.split()
		resolution.append(line[1])
		timing_parameters.append(line[2:11])


def print_resolution():
	for i in range(len(resolution)):
		print(resolution[i])
		print("timing_para:")
		temp=timing_parameters[i]
		print("refresh (Hz) =" + temp[0] + " hdisp=" + temp[1] + " hss=" + temp[2] +  " hse=" + temp[3] + " htot=" + temp[4] + " vdisp=" + temp[5] + " vss=" + temp[6] + " vse=" + temp[7] + " vtot=" + temp[8] )	
		print("\n")


def sort_resolution():
	global resolution
	global timing_parameters
	temp_list=[]
	temp_list2=[]
	for i in range(len(resolution)-1):
		if resolution[i] not in temp_list:
			temp_list.append(resolution[i])
			temp_list2.append(timing_parameters[i])
	resolution=temp_list
	timing_parameters=temp_list2


find_resolution()
print_resolution()
print("--------------------")
sort_resolution()
print_resolution()
