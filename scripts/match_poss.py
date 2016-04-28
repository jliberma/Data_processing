#!/usr/bin/env python

###############################################
# match_possession - parse IRB 7s match reports
# written by jliberman@utexas.edu
###############################################

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
    outfile = '{}_{}_{}_poss.txt'.format(parts[4], parts[1], parts[0])
    pagenos = set([0,0])
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
        for line in islice(start_at, 1, None):
	    if 'Printed' in line:
		break
	    elif '( ' in line or ':' in line:
		txtout.write(line)
	    else:
		pass

    return outfile


# convert text to csv
def write_csv(txt):
    
    # create output filename
    event = txt.split("_")[0]
    match = txt.split("_")[1]
    outfile = '{}_{}_possession.csv'.format(event, match)

    # parse text to dictionary lists
    with open(txt, 'r') as in_txt:
	lines = in_txt.readlines()

    # write to csv
    with open(outfile, 'wb') as out_csv:
        csv = writer(out_csv)
	if '(' in lines[1]:
		if int(lines[0].split('(')[1].strip(' \n)')) > int(lines[1].split('(')[1].strip(' \n)')):
			line = [
			event,
			match,
			lines[0].split('(')[0].strip(),
			lines[0].split('(')[1].strip(' \n)'),
			lines[4].strip(),
			lines[1].split('(')[0].strip(),
			lines[1].split('(')[1].strip(' \n)'),
			lines[7].strip()
			]
		else:
			line = [
			event,
			match,
			lines[1].split('(')[0].strip(),
			lines[1].split('(')[1].strip(' \n)'),
			lines[7].strip(),
			lines[0].split('(')[0].strip(),
			lines[0].split('(')[1].strip(' \n)'),
			lines[4].strip()
			]
	else:
		if int(lines[0].split('(')[1].strip(' \n)')) > int(lines[4].split('(')[1].strip(' \n)')):
			line = [
			event,
			match,
			lines[0].split('(')[0].strip(),
			lines[0].split('(')[1].strip(' \n)'),
			lines[3].strip(),
			lines[4].split('(')[0].strip(),
			lines[4].split('(')[1].strip(' \n)'),
			lines[7].strip()
			]
		else:
			line = [
			event,
			match,
			lines[4].split('(')[0].strip(),
			lines[4].split('(')[1].strip(' \n)'),
			lines[7].strip(),
			lines[0].split('(')[0].strip(),
			lines[0].split('(')[1].strip(' \n)'),
			lines[3].strip()
			]
	csv.writerow(line)


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
