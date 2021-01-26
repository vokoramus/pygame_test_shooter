import csv

with open('players.csv') as f:
    reader = csv.reader(f) 

for row in reader:  # csv.reader = iterator
print(row)
