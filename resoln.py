import subprocess
import time

resolution=[]
resolution_number=25

string1='#0'
for i in range(resolution_number):
	output = subprocess.check_output("cat modetest | grep -m 1 '\#'" + str(i), shell=True)
	temp = output.decode("utf-8")
	#print(temp)
	table=temp.split()
	resolution.append(table[1])

a=len(resolution)
print("supported resolutions are:")
for i in range(a):
	print(resolution[i])	
	


	
