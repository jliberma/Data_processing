#!/usr/bin/env python

##############################################
# match_penalty - parse IRB 7s penalty reports 
# written by jliberman@utexas.edu
##############################################

import os
import sys

from contextlib import closing
from csv import writer
from itertools import dropwhile, islice, izip
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


# convert PDF to text
def write_txt(pdf_filename):
    parts = pdf_filename.split("_")
    outfile = '{}_{}_{}.txt'.format(parts[4], parts[1], parts[0])
    pagenos = set([1,2])
    rsrcmgr = PDFResourceManager(caching=True)

    with open(outfile, 'w') as txtout:
	with closing(TextConverter(rsrcmgr, txtout, codec='utf-8', laparams=LAParams())) as device:
	    with file(pdf_filename, 'rb') as pdfin:
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                for page in PDFPage.get_pages(pdfin, pagenos):
                    interpreter.process_page(page)

    # remove header/footer
    with open(outfile, 'r') as txtin:
        lines = txtin.read().splitlines(True)
    with open(outfile, 'w') as txtout:
        start_at = dropwhile(lambda line: not line.startswith('Referee'), lines)
        for line in islice(start_at, 0, None):
	    if 'Page' in line or line == "\n" or 'Summary' in line:
		pass
	    elif 'Printed' in line:
		break
	    else:
	    	txtout.write(line)

    return outfile


# convert text to csv
def write_csv(txt):
    
    out = {}
    out['match'] = []
    out['event'] = []
    out['ref'] = []

    # create output filename
    event = txt.split("_")[0]
    match = txt.split("_")[1]
    outfile = '{}_{}_penalty.csv'.format(event, match)

    # parse text to dictionary lists
    with open(txt, 'r') as in_txt:
        lines = (line for line in in_txt)
        for line in lines:
	    if line.startswith(('H\n', "Description\n", "Time\n", "Team\n", "Reason\n")):
	            header = line.strip()
		    out[header] = []
	    elif line.startswith('Referee'):
	        ref = line.split(' ', 1)[1]
	        ref = ref.replace(',','').strip()
	    else:
		    out[header].append(line.strip('\n'))

    # populate match & event dictionary lists
    for x in out[header]:
        out['match'].append(match)
        out['event'].append(event)
        out['ref'].append(ref)

    # write to csv
    #headers = ['Event','Match','Ref','Half','Time','Team','Description','Reason']
    with open(outfile, 'w') as out_csv:
        csv = writer(out_csv)
	#csv.writerow(headers)
        for row in izip(out['event'], out['match'], out['ref'], out['H'], out['Time'], out['Team'], out['Description'], out['Reason']):
            csv.writerows([row])


def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <pdf>\n" % (argv[0],))
	return 1

    if not os.path.exists(argv[1]):
	sys.stderr.write("ERROR: %s not found.\n" % (argv[1],))
        return 1

    txt = write_txt(argv[1])
    write_csv(txt)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
