
# Compute the MD5 sums for the two files
sum1 = 'a7c44c41b5062cbbde1688689020b417c687cd7a'
sum2 = 'e5b235c4b7e931f4c5c088af508cc86d86d1a265'

bytes_sum1 = []
for i in range(len(sum1)):
    bytes_sum1.append('{0:016b}'.format(sum[i]))
    

bytes_sum2 = '{0:016b}'.join(format(ord(x), 'b') for x in sum2)
print(bytes_sum1)
print(len(bytes_sum1))
print(len(bytes_sum2))
# Count the number of different bits in the two sums
num_bits = len(sum1) * 8  # Each hexadecimal digit represents 4 bits, so there are 4 * len(sum1) bits in total
num_different_bits = 0
for i in range(0,len(bytes_sum1),8):
    for k in range(8):
        if bytes_sum1[i+k] != bytes_sum2[i+k]:
        
        # The two hexadecimal digits are different, so count the number of different bits
        # in the corresponding byte
            num_different_bits += 1

# Calculate the percentage of different bits
percent_different = num_different_bits / num_bits * 100
print('Percentage of different bits:', percent_different)
