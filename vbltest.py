import subprocess
import os
import signal
import time

table=[]
cmd = "cat vbltest | grep freq:"

output = subprocess.check_output(cmd, stdin=subprocess.PIPE, shell=True, preexec_fn=os.setsid)		
#time.sleep(5)
#os.killpg(os.getpgid(output.pid), signal.SIGTERM)
output=output.decode('utf-8')
output=output.split()
for i in range(1,len(output),2):
	table.append(output[i])

print("command output= " + cmd)
for i in table:
	print(i)

max_val=max(table)
maxval=max_val[0:5]
maxval2=float(maxval)
new = round(maxval2)
print(maxval2, new)	