import subprocess
import time
import os 
import signal

s1 = 'Connectors:'
s2 = 'CRTCs:'
s3 = 'Planes:'
s4 = 'formats:'
table=[]

def getpara(string1):   
	print("finding id value of " + string1) 
	output = subprocess.check_output("modetest -M NB2 | grep -A 2 " + string1, shell=True)
	temp = output.decode("utf-8")
	table1=temp.split()
	#print(table)
	for i in table1:
		a=i.isnumeric()
		if a==True:
			print(string1)
			print(i)
			return i

def getformat(string1):
	global table
	print("finding Formats available ") 
	output = subprocess.check_output("modetest -M NB2 | grep -m 1 " + string1, shell=True)
	temp = output.decode("utf-8")
	#print(temp)
	table=temp.split()
	#print(table)
	table.pop(0)

def validate():
	global table
	a=len(table)
	for i in range(a):
		cmd = "modetest -M NB2 -s " + conn_id + "@" + encod_id + ":640x480@" + table[i] + " -P " + "33@" + encod_id + ":200x200+30+30"
		print("testing for cmd: Mode + plane :" + cmd)
		output = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)		
		print("checkig output......")
		time.sleep(15)
		os.killpg(os.getpgid(output.pid), signal.SIGTERM)			
		print("terminated")	
		print("\n")

conn_id = getpara(s1)	

encod_id = getpara(s2)

plane_id = getpara(s3)

getformat(s4)
print(table)

validate()





