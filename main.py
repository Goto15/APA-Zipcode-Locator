# from address import AddressParser, Address
import csv

with open('addresses.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

    for row in reader:
        if(len(row) > 3):
            tempAddress = ' '.join(row[0: -3])
            print(tempAddress, row[-2])
