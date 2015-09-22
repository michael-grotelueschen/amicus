import os

def convert_pdfs_to_dirty_text_files():
    """Use Apache Tika to convert oral argument transcript pdfs to txt files."""
    input_filenames = os.listdir('pdfs/')
    for input_filename in input_filenames:
        output_filename = 'txts_dirty/'
        output_filename += input_filename.replace('pdf', 'txt')

        # The tika command is:
        # java -jar ../tika-app-1.10.jar --text [input file]
        tika_command = "java -jar ../tika-app-1.10.jar --text "
        tika_command += '%s%s ' % ('pdfs/', input_filename)
        tika_command += '> %s' % output_filename
        os.system(tika_command)

def clean_text_files():
    """Clean up every dirty txt file using strip_lines().
    Write the results to files.
    """
    input_filenames = os.listdir('txts_dirty/')
    for input_filename in input_filenames:
        lines = strip_lines('txts_dirty/' + input_filename)

        output_filename = 'txts_clean/' + input_filename
        with open(output_filename, 'w') as f:
            for line in lines:
                f.write(line + '\n')

def strip_lines(filename=None):
    """Clean up dirty txt file:

    1) replace all unicode byte strings with regular strings
    2) delete all empty lines or lines only containing newlines
    3) delete all line numbers and page numbers
    4) delete all references to Anderson Reporting Company
       (name, address, phone number)
    5) delete all boilerplate
    6) delete appendix

    Then return a list of cleaned strings.
    """
    space_byte = '\xc2\xa0'
    hyphen_byte = '\xc2\xad'
    t1 = 'Official'
    t2 = 'Alderson Reporting Company'
    t3 = '1111 14th Street'
    t4 = 'Suite 400 Washington'
    t5 = 'DC 20005'
    t6 = '1-800-FOR-DEPO'
    
    lines = []
    with open(filename) as f:
        # BEWARE:
        # An incorrect reached_end condition can cause an infinite loop.
        reached_end = False
        while not reached_end:
            line = f.readline()
            # remove: unicode byte: '\xc2\xa0' == ' '
            #         unicode byte: '\xc2\xad' == '-'
            #         leading and trailing whitespace
            line = line.replace(space_byte, ' ')
            line = line.replace(hyphen_byte, '-')
            line = line.strip()
            # remove all traces of the Alderson Reporting Company
            if t1 in line or \
               t2 in line or \
               t3 in line or \
               t4 in line or \
               t5 in line or \
               t6 in line:
                line = ''
            # ignore lines that are too short to be meaningful
            # remove leading digits
            # remove leading and trailing whitespace
            if 3 < len(line):
                if line[0].isdigit():
                    line = line[1:]
                if line[0].isdigit():
                    line = line[1:]
                line = line.strip()
                lines.append(line)
            # Check if we have reached the end of the argument.
            # (We don't want to include the appendix.)
            #
            # The last two conditions are for:
            #     case 14556 part 1
            #     case 03-1693
            if line.startswith('(Wher') or \
                line.startswith('[Wher') or \
                line.startswith('[ Wher') or \
                line.startswith('Whereupon,') or \
                '(Short break at 11:32 a.m.)' in line or \
                'now adjourned until Monday next at 10' in line:
                reached_end = True
    return lines

if __name__ == "__main__":
    clean_text_files()