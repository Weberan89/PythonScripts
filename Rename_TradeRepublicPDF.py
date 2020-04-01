###########################################################################
##
##      Rename PDF exports from TradeRepublic
##      v01.00
##
###########################################################################

import sys
import os
import re
import PyPDF4
from datetime import datetime
from tkinter import filedialog, Tk

# Open File choser
Tk().withdraw()
files2iter = filedialog.askopenfilenames(title='Choose PDF-files to convert Name of TradeRepublic pdfs', \
                                         filetypes=[('PDF', '*.pdf')])
print( str(len(files2iter)) + ' files will be renamed:\n' )
# Iterate over all chosen files
for cur_file_path in files2iter:
    error=False
    # Open PDF
    cur_file = open(cur_file_path, 'rb')
    try:
        pdffile = PyPDF4.PdfFileReader(cur_file)

        # Get count of pages and iterate over all pages till key was found
        cnt_of_pages = pdffile.getNumPages()
        cur_date = '20xxxxxx'

        for i in range(0, cnt_of_pages):
            # Read current page and get text
            cur_page = pdffile.getPage(i)
            cur_text = cur_page.extractText()

            # Get Date from page
            match = re.search(r'\d{2}.\d{2}.\d{4}', cur_text)
            if match:
                date = datetime.strptime(match.group(), '%d.%m.%Y').date()
                cur_date = date.isoformat().replace('-', '')

            # Check for keywords
            if 'Steuerbescheinigung' in cur_text:
                # Zeitraum xx.xx.xxxx
                match = re.search(r'Zeitraum \d{2}.\d{2}.\d{4}', cur_text)
                year = match.group()[-4:]
                Filename_Info = 'Steuerbescheinigung_' + str(year)
                break
            elif 'Order Verkauf' in cur_text:
                idx_start = re.search('BETRAG', cur_text).end() + 1
                aktie = cur_text[idx_start:idx_start + re.search(' ', cur_text[idx_start:idx_start + 20]).start()]
                Filename_Info = 'Verkauf_' + aktie
                break
            elif 'Order Kauf' in cur_text:
                idx_start = re.search('BETRAG', cur_text).end() + 1
                aktie = cur_text[idx_start:idx_start + re.search(' ', cur_text[idx_start:idx_start + 20]).start()]
                Filename_Info = 'Kauf_' + aktie
                break
            elif 'KONTOSTAND AM' in cur_text:
                match = re.search(r'AM \d{2}.\d{2}.\d{4}', cur_text)
                if match:
                    year = match.group()[-4:] + match.group()[6:8] + match.group()[3:5]
                else:
                    year = '20xxxxxx'
                Filename_Info = 'Kontoauszug_' + str(year)
                break
            else:
                Filename_Info = 'NotImplementedYet'

        # Create output name
        idx_last_folder = cur_file_path.rfind('/')+1
        cur_outfile_path = cur_file_path[:idx_last_folder] + cur_date + '_' + Filename_Info + '.pdf'

    except Exception as e:
        print(e)
        error = True
        cur_file.close()
        exit()

    cur_file.close()
    print( '  ' + cur_file_path + ' -> ' + cur_outfile_path)
    os.rename(cur_file_path, cur_outfile_path)

