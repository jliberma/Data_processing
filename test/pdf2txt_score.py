#!/usr/bin/python
import sys
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

def main(argv):
    fname = '2014_Dubai_7s_Match_2_Wales_vs_Canada.pdf'	# pass input filename as param
    outfile = 'test.txt'				# create outfile name
    pagenos = set([2,3])				# get only page 3 (scoring)

    codec = 'utf-8'
    caching = True
    laparams = LAParams()

    rsrcmgr = PDFResourceManager(caching=caching)
    outfp = file(outfile, 'w')
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    fp = file(fname, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos):
        interpreter.process_page(page)
    fp.close()
    device.close()
    outfp.close()

    with open(outfile) as datafile:
        lines = datafile.readlines()
        #open('test2.txt', 'w').writelines(lines[8:-8])
        open(datafile, 'w').writelines(lines[8:-8])

    return

if __name__ == '__main__': sys.exit(main(sys.argv))
