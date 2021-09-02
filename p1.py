import linecache



s1 = 'Connectors:'
s2 = 'Encoders:'
s3 = 'Planes:'
s4 = 'formats:'


def frames(string1):
	file1 = open('ModeTest', 'r')
	content = file1.readlines()

	flag = 0
	index = 0	
	
	for line in content:  
		index += 1

		if string1 in line:
			flag = 1
			break 
	     

	     	
	if flag == 0: 
	   	print('String', string1 , 'Not Found') 
	else:
		print(string1) 
		lines = linecache.getline('ModeTest',index)	 
		print(lines[10:])   
		
	print('\n')	    
	file1.close() 



def findparam(string1):
	
	file1 = open('ModeTest', 'r')
	content = file1.readlines()

	flag = 0
	index = 0	
	
	for line in content:  
		index += 1

		if string1 in line:
			flag = 1
			break 
	     

	     	
	if flag == 0: 
	   print('String', string1 , 'Not Found') 
	else:
		print(string1) 
		for i in range (index+1,index+3):
			lines = linecache.getline('ModeTest',i)	 
			 		
			print(lines[:4]) 
		
	print('\n')	    
	file1.close() 


findparam(s1)
findparam(s2)
findparam(s3)
frames(s4)
