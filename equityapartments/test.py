  
import re 

ini_str = '/guestcard/b4213/tour#/booktourunit/newtour/3/2/S/512/5003/3 Bedroom AB/1306/1/3'
sub_str = "/"
occurrence = 9
  
  
# Finding nth occurrence of substring 
val = -1
for i in range(0, occurrence): 
    val = ini_str.find(sub_str, val + 1) 
       
# Printing nth occurrence 
print ("Nth occurrence is at", val)
print(ini_str[val + 1:val+4])

# '/guestcard/b4213/tour#/booktourunit/newtour/3/2/S/512/5003/3 Bedroom AB/1306/1/3'
# '/guestcard/b4213/tour#/booktourunit/newtour/3/2/S/518/5003/3
# '/guestcard/b4213/tour#/booktourunit/newtour/3/2/S/612/5199/3 Bedroom AB/1306/1/3'