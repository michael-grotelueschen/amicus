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

def strip_lines(filename='14-556q1_l5gm.txt'):
    lines = []
    with open(filename) as f:
        for line in f:
            # remove unicode byte: '\xc2\xa0' == ' '
            # remove unicode byte: '\xc2\xad' == '-'
            # remove leading and trailing whitespace
            # remove 'Official'
            # remove 'Alderson Reporting Company'
            new_line = line.replace('\xc2\xa0', ' ')
            new_line = new_line.replace('\xc2\xad', '-')
            new_line = new_line.strip()
            new_line = new_line.replace('Official', '')
            new_line = new_line.replace('Alderson Reporting Company', '')

            # ignore lines that are too short to be meaningful
            # remove leading digits
            # remove leading and trailing whitespace
            if 3 < len(new_line):
                if new_line[0].isdigit():
                    new_line = new_line[1:]
                if new_line[0].isdigit():
                    new_line = new_line[1:]
                new_line = new_line.strip()

                lines.append(new_line)
    return lines


if __name__ == "__main__":
    convert_pdfs_to_dirty_text_files()

    