x = [41, 31]

# Calculate the sum of values in x
sum_x = sum(x)

# Initialize sigfile as a list with the desired length
sigfile = [0] * (sum_x)

# print(sigfile)
query_bitmap = 0
for i in x:
    sigfile[i] = 1

    query_bitmap |= (1 << i)
    print(query_bitmap)


# sigfile.reverse()

# print(sigfile)


