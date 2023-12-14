import pandas as pd

with open('input_1.txt', 'r') as f:
    lines = f.readlines()
    lines = [l.strip() for l in lines]

counter = []
count = 0
max = 0
for l in lines:
    if l == '':
        count = 0
    else:
        count += int(l)
    counter.append(count)
    if count > max:
        max = count
print(max)