import random

f = open("data.dat", "w")
N = 10

f.write(str(N) + "\n")
for i in range(N):
    data = str(random.randint(10 ** 7, 5 * 10 ** 8))
    task = str(random.randint(10 ** 9, 10 ** 12))
    locationX = str(random.randint(10, 20))
    locationY = str(random.randint(10, 20))
    f.write("%s,%s,%s,%s\n" % (data, task, locationX, locationY))
