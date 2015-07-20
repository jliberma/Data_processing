# convert the PDF to text
# get only the part of the text I want
# extract event and match number from the PDF title
# create dictionary lists
# combine dictionary lists to rows
# add event and match columns to rows
# write to csv named with event and match number
# execute the conversion and parsing in parallel
# put everything into a database

import csv
import itertools
import glob

out = {}
event = []
match = []

for pdf in glob.glob("*.pdf"):
	print pdf

# create dictionary of lists
with open('d2.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line for line in stripped if line)
    for line in lines:
	if line.startswith(('H', "Description", "Time", "Team")):
		header = line.strip()
		out[header] = []
	else:
		out[header].append(line.strip('\n'))

#print str(out)		# print contents of the dictionary
#print len(out['H']) 	# length of the values in the dictionary

# create event and match lists
for i in out['H']:
	event.append("Dubai")
	match.append("2")

# combine lists into csv file
with open('d2.csv', 'w') as out_file:
        writer = csv.writer(out_file)
	writer.writerow(("Event","Match","Half","Time","Team","Type"))
	for row in itertools.izip(event, match, out['H'], out['Time'], out['Team'], out['Description']):
        	writer.writerows([row])
