import subprocess
import time

resolution=[]
timing_parameters=[]
max_res=0


def find_resolution():
	temp=[]
	global resolution
	global max_res
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
	for i in range(max_res):
		print(resolution[i])
		print("timing_para:")
		temp=timing_parameters[i]
		print("refresh (Hz) =" + temp[0] + " hdisp=" + temp[1] + " hss=" + temp[2] +  " hse=" + temp[3] + " htot=" + temp[4] + " vdisp=" + temp[5] + " vss=" + temp[6] + " vse=" + temp[7] + " vtot=" + temp[8] )	
		print("\n")


find_resolution()
print_resolution()