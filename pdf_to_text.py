# pdfs/02-1472.pdf
#
# 02-472.txt
#
# tika command:
# 
# java -jar ../tika-app-1.10.jar --text [input file]
# 
# 
# TEXT PARSING TO DO:
# 
# 1) replace all unicode byte strings with strings
# 2) delete all newlines
# 3) delete all line numbers and line numbers
# 4) delete all references to Anderson Reporting Company
# 5) delete all boilerplate
# 6) delete appendix
# 7) INTERRUPTIONS?
# 
# 
#
# '\xc2\xa0' == ' '
# '\xc2\xad' == '-'
#
#

import os

def convert_pdfs_to_dirty_text_files():
    input_filenames = os.listdir('pdfs/')
    for input_filename in input_filenames:
        output_filename = 'txts_dirty/'
        output_filename += input_filename.replace('pdf', 'txt')

        tika_command = "java -jar ../tika-app-1.10.jar --text " #[input file]
        tika_command += '%s%s ' % ('pdfs/', input_filename)
        tika_command += '> %s' % output_filename
        os.system(tika_command)    

def strip_lines(filename=None):
    lines = []
    with open(filename) as f:
        reached_end = False
        while not reached_end:
            line = f.readline()
            # remove: unicode byte: '\xc2\xa0' == ' '
            #         unicode byte: '\xc2\xad' == '-'
            #         leading and trailing whitespace
            #         'Official'
            #         'Alderson Reporting Company'
            #         '1111 14th Street NW, Suite 400 Washington, DC 20005'
            line = line.replace('\xc2\xa0', ' ')
            line = line.replace('\xc2\xad', '-')
            line = line.strip()
            line = line.replace('Official', '')
            line = line.replace('Alderson Reporting Company', '')
            line = line.replace('1111 14th Street NW, Suite 400 Washington, DC 20005', '')

            # ignore lines that are too short to be meaningful
            # remove leading digits
            # remove leading and trailing whitespace
            # convert to lowercase
            if 3 < len(line):
                if line[0].isdigit():
                    line = line[1:]
                if line[0].isdigit():
                    line = line[1:]
                line = line.strip()
                #line = line.lower()
                lines.append(line)

            # Check if we have reached the end of the argument.
            # (Before we have reached the appendix.)
            if 'The case is submitted.' in line:
                reached_end = True
                print 'REACHED END'
    return lines


if __name__ == "__main__":
    filename = '13-7120_hd1a.txt'
    #lines = strip_lines(filename)