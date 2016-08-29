#while continue break
while true:
	s == input("enter a word")
	if s == "quit":
		break
	elif len(s)<3:
		continue
	print 'input is of sufficient length'
