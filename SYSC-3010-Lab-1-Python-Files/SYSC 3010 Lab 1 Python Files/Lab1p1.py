#Denise Mayo 101044064 - THIS CODE IS NOT MINE

import string
import random
# create a list of 4 characters
secret = [random.choice('ABCDEF') for item in range(4)]
# tell the player what is going on
print("I've selected a 4-character secret code from the letters
A,B,C,D,E and F.")
print("I may have repeated some.")
print("Now, try and guess what I chose.")
yourguess = []
while list(yourguess) != secret:
 yourguess = input("Enter a 4-letter guess: e.g. ABCD : ").upper()
 if len(yourguess) != 4:
 continue
 # turn the guess into a list, like the secret
 print("You guessed ", yourguess)
 # create a list of tuples comparing the secret with the guess
 comparingList = zip(secret, yourguess)
 # create a list of the letters that match
 # (this will be 4 when the lists match exactly)
 correctList = [speg for speg, gpeg in comparingList if speg
== gpeg]
 # count each of the letters in the secret and the guess
 # and make a note of the fewest in each
 fewestLetters = [min(secret.count(j), yourguess.count(j)) for
j in 'ABCDEF']
 print("Number of correct letter is ", len(correctList))
 print("Number of unused letters is ", sum(fewestLetters) -
len(correctList))
print("YOU GOT THE ANSWER : ", secret)
