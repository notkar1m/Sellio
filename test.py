import random

random_number = random.randint(1,2)

myGuess = input("Guess the number")

if int(myGuess) == random_number:
	print("Correct")
else:
	print("Incorrect")





