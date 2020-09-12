bsp = [(7, 35), (36, 51), (37, 6), (1, 20), (25, 2), (35, 15), (7, 35),
(5, 21), (16, 74), (5, 53), (25, 47), (17, 78), (18, 62), (7, 76), (5, 21)]


sorted_by_second = sorted(bsp, key=lambda tup: tup[0])

bsp.remove((7,35))

print(bsp)
print(sorted_by_second)