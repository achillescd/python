#file name if.py
number=23
guess=int(input('Enter a number'))
if guess == number:
	print ('Equal')
elif guess < number:
	print ('less')
else:
	print ('More')
print ('Done')