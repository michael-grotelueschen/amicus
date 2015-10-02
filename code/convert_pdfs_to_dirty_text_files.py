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

if __name__ == "__main__":
    convert_pdfs_to_dirty_text_files()