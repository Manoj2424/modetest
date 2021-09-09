import subprocess
import time

resolution=[]
timing_parameters=[]
resolution_number=25

for i in range(resolution_number):
	output = subprocess.check_output("cat modetest | grep -m 1 '\#'" + str(i), shell=True)
	temp = output.decode("utf-8")
	#print(temp)
	table=temp.split()
	resolution.append(table[1])
	timing_parameters.append(table[2:11])

print(resolution)
a=len(resolution)
print("supported resolutions are:")
for i in range(a):
	print(resolution[i])
	print("timing_para:")
	temp=timing_parameters[i]
	#temp.split()
	print("refresh (Hz) =" + temp[0] + " hdisp=" + temp[1] + " hss=" + temp[2] +  " hse=" + temp[3] + " htot=" + temp[4] + " vdisp=" + temp[5] + " vss=" + temp[6] + " vse=" + temp[7] + " vtot=" + temp[8] )	
	print("\n")
