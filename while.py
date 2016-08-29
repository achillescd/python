#file name while.py
number = 23
opt = 1
while opt:
	guess = input("Enter a number:")
	if guess == number:
		print ('Equal')
	elif guess < number:
		print ('less')
	else:
		print ('More')
print ('Done')