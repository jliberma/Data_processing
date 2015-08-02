#!/usr/bin/env python

###########################################
#
# match_report - parse IRB 7s match reports 
#
# written by jliberman@utexas.edu
#
###########################################

import csv
import itertools
import glob
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
    outfile = pdf.split("_")[4] + "_" + \
        pdf.split("_")[1] + "_" + pdf.split("_")[0] + ".txt"
    pagenos = set([2,3])

    codec = 'utf-8'
    caching = True
    laparams = LAParams()

    rsrcmgr = PDFResourceManager(caching=caching)
    # try with statement here
    outfp = file(outfile, 'w+')
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    fp = file(pdf, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos):
        interpreter.process_page(page)
    fp.close()
    device.close()

    #with open(outfp, 'r') as txt_file:
        #lines = txt_file.readlines()
    outfp.seek(0, 0)
    lines = outfp.readlines()
    #outfp.seek(0, 0)
    outfp.writelines(lines[8:-8])
        #open('test2.txt', 'w').writelines(lines[8:-8])
        #datafile.writelines(lines[8:-8])
    outfp.close()

    # return outfile name
    return


# parse text to dictionary lists
def parse_text():
    out = {}
    with open('d2.txt', 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line for line in stripped if line)
        for line in lines:
	    if line.startswith(('H', "Description", "Time", "Team")):
	            header = line.strip()
		    out[header] = []
	    else:
		    out[header].append(line.strip('\n'))
    return    


# write lists to a csv file
def write_csv():
    event = []
    with open('d2.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(("Event","Match","Half","Time","Team","Type"))
        # join event, match, and dictionary lists to row
        for row in itertools.izip(event, match, out['H'], out['Time'], out['Team'], out['Description']):
        # write to csv named with event and match number
            writer.writerows([row])
    return


def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <pdf>\n" % (argv[0],))
	return 1

    if not os.path.exists(argv[1]):
	sys.stderr.write("ERROR: %s not found.\n" % (argv[1],))
        return 1

    write_txt(argv[1])

if __name__ == '__main__':
    sys.exit(main(sys.argv))
