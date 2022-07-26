#! /usr/bin/env python3

import pdb
import argparse
import logging
import fitz
import json

def scan_pdf(file):
    '''Scans a given PDF, returns data'''

    # Use fitz to parse out the PDF
    doc = fitz.open(file)
    page1 = doc[0]
    words = page1.get_text("words")

    data = {}

    # Take the first two words as the date and time
    data['Record_DateTime'] = words[0][4] + " " + words[1][4]

    #
    # Search for "Name", everything after it on the line is the name.
    #
    name_pos = page1.search_for("Name:")

    # Draw a square from the same line name is found to the edge of the page
    x0 = name_pos[0][0]
    y0 = name_pos[0][1]
    x1 = page1.bound()[2]
    y1 = name_pos[0][3]

    # get all words in that square
    name_coord = fitz.Rect(x0,y0,x1,y1)
    name_line = [w[4] for w in words if fitz.Rect(w[:4])in name_coord]

    # drop the "Name:" as we don't care about that, the remaning elements is the name
    name_line.remove('Name:')
    data['Name'] = " ".join(name_line)

    #
    # TODO: work out how to find out coords dynamically for this
    # Parse the table into an array, from the 15th word onwards, line by line
    #
    # data['Table'] = []
    # for i in range(15,len(words) -1 ):

    #     line = []
    #     line_position = words[i][3]

    #     pdb.set_trace()

    # pdb.set_trace()

    return data

# def write_csv(data,file):
#    '''Writes data out to a csv'''

def run():
    '''Main run loop'''

    pdf_data={}

    # Extract data from each file:
    for file in cli_args.files:

        # Skip if it's not a pdf file
        if not file.endswith('.pdf'):
            log.warning("Skipping: " + file + " As it's not a .pdf")
            continue

        pdf_data[file] = scan_pdf(file)

    return pdf_data

if __name__ == "__main__":

    log = logging.getLogger()

    parser = argparse.ArgumentParser(description='Extract data from a PDF into a csv')
    parser.add_argument("files", nargs='+', help="PDF files to try and convert")
    cli_args = parser.parse_args()

    log.info("Starting")
    results = run()

    print(json.dumps(results,indent=4))
