#!/usr/bin/env python

###########################################
# match_report - parse IRB 7s match reports 
# written by jliberman@utexas.edu
###########################################

import csv
import itertools
import os
import sys

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


# convert the PDF to text
def write_txt(pdf):
    outfile = pdf.split("_")[4] + "_" + pdf.split("_")[1] + "_" + \
        pdf.split("_")[0] + ".txt"
    pagenos = set([2,3])

    codec = 'utf-8'
    caching = True
    laparams = LAParams()

    rsrcmgr = PDFResourceManager(caching=caching)
    outfp = file(outfile, 'w+')
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    fp = file(pdf, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos):
        interpreter.process_page(page)
    fp.close()
    device.close()
    outfp.close()

    # remove header and footer from text file
    with open(outfile, 'r') as txtin:
        lines = txtin.read().splitlines(True)
    with open(outfile, 'w') as txtout:
        txtout.writelines(lines[8:-8])

    return outfile

# convert text to csv
def write_csv(txt):
    
    out = {}
    out['match'] = []
    out['event'] = []

    # create output filename
    event = txt.split("_")[1]
    match = txt.split("_")[0]
    outfile = match + "_" + event + "_" + "scoring" + ".csv"

    # parse text to dictionary lists
    with open(txt, 'r') as in_file:
        lines = (line.strip() for line in in_file)
        for line in lines:
	    if line.startswith(('H', "Description", "Time", "Team")):
	            header = line.strip()
		    out[header] = []
	    else:
		    out[header].append(line.strip('\n'))

    # populate match & event dictionary lists
    for x in out[header]:
        out['match'].append(match)
        out['event'].append(event)

    # write to the csv
    with open(outfile, 'w') as out_file:
        writer = csv.writer(out_file)
	writer.writerow(("Event","Match","Half","Time","Team","Type"))
        for row in itertools.izip(out['event'], out['match'], out['H'], out['Time'], out['Team'], out['Description']):
            writer.writerows([row])
    
    return


def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <pdf>\n" % (argv[0],))
	return 1

    if not os.path.exists(argv[1]):
	sys.stderr.write("ERROR: %s not found.\n" % (argv[1],))
        return 1

    txt = write_txt(argv[1])
    csv = write_csv(txt)

    return

if __name__ == '__main__':
    sys.exit(main(sys.argv))
