from random import randrange, seed

seed(2022)

total = 20
a = open("seeds.txt", "w")
for i in range(total):
	seedNumber = randrange(100000)
	print(seedNumber)
	a.write(str(seedNumber)+"\n")
a.close()