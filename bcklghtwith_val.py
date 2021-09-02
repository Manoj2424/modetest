import subprocess
import os
import time

backlight_path = '/sys/class/backlight/intel_backlight/'
brightness= '/sys/class/backlight/intel_backlight/brightness'
actual_brightness = '/sys/class/backlight/intel_backlight/actual_brightness'
brightness_max_range=255

print("checking for path:")
if os.path.exists(backlight_path):
	
	print("\n")	

	print("Path " + backlight_path + " found:")

	print("\n")	

	x = range(0, brightness_max_range+1, 15)
	for  brightness_range in x:
		
		print("Testing brightness value :" + str(brightness_range))
		op1=subprocess.call("sudo echo " + str(brightness_range) + "> " + brightness,shell=True)
		print("brightness is set | verifying brightness")
		time.sleep(2)
		o1=subprocess.check_output("cat " + actual_brightness, shell=True)
		#print(o1)
		o2=subprocess.check_output("cat " + brightness, shell=True)
		#print(o2)

		if o1==o2:
			print("brightness set sucessfull for: " + str(brightness_range))
		else:
			print("unsecessfull")

		print("\n")	
	
else:
	print("path not found")

