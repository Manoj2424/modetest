import subprocess
import os
import time

backlight_path = '/sys/class/backlight/intel_backlight/'
brightness= '/sys/class/backlight/intel_backlight/brightness'
actual_brightness = '/sys/class/backlight/intel_backlight/actual_brightness'
brightness_range=['1000','2000','3000','4000','5000','6000','7000','7500']

print("checking for path:")
if os.path.exists(backlight_path):
	
	print("\n")	

	print("Path " + backlight_path + " found:")

	print("\n")	

	a=len(brightness_range)

	for i in range(a):
		
		print("Testing brightness value :" + brightness_range[i])
		op1=subprocess.call("sudo echo " + brightness_range[i] + "> " + brightness,shell=True)
		print("brightness is set | verifying brightness")
		time.sleep(2)
		o1=subprocess.check_output("cat " + actual_brightness, shell=True)
		#print(o1)
		o2=subprocess.check_output("cat " + brightness, shell=True)
		#print(o2)

		if o1==o2:
			print("brightness set sucessfull for: " + brightness_range[i])
		else:
			print("unsecessfull")

		print("\n")	
	
else:
	print("path not found")

