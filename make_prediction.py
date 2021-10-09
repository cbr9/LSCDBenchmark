import sys
import csv
from collections import defaultdict

[_, option, data, dataset, outfile] = sys.argv

with open(data, encoding='utf-8') as csvfile: 
    reader = csv.DictReader(csvfile, delimiter='\t',quoting=csv.QUOTE_NONE,strict=True)
    table = [row for row in reader]

if option == 'gold':
    output_data = table

with open(outfile, 'w') as f:  
    w = csv.DictWriter(f, output_data[0].keys(), delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')
    w.writeheader()
    w.writerows(output_data)


