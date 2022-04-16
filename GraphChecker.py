import random
letters = ['A','B','C','D','E','F','G','H']
for i in range(50):
    letter1 = random.choice(letters)
    letter2 = random.choice(letters)
    print(letter1,letter2)