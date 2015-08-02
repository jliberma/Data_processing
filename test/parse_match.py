# execute the conversion and parsing in parallel
# put everything into a database

import csv
import itertools
import glob

out = {}
event = []
match = []

# write a function that takes a pdf file as input

# extract event and match number from the PDF title
for pdf in glob.glob("*.pdf"):
	match = pdf.split("_")[4] 
	event = pdf.split("_")[1]
	filename = match + "_" + event + ".txt"

# convert the PDF to text
# get only the part of the text I want

# create dictionary lists
with open('d2.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line for line in stripped if line)
    for line in lines:
	if line.startswith(('H', "Description", "Time", "Team")):
		header = line.strip()
		out[header] = []
	else:
		out[header].append(line.strip('\n'))

# combine lists into csv file
with open('d2.csv', 'w') as out_file:
        writer = csv.writer(out_file)
	writer.writerow(("Event","Match","Half","Time","Team","Type"))
	# join event, match, and dictionary lists to row
	for row in itertools.izip(event, match, out['H'], out['Time'], out['Team'], out['Description']):
		# write to csv named with event and match number
        	writer.writerows([row])
