# Possible features:
# 1) Oral arguments:
#  1)  interruptions
#  2)  word counts
#  3)  laughter
#  4)  how many justices interact with a side
#  5)  how many questions justices ask a side
#  6)  key (positive/negative) words for petitioners/respondents
#  7)  key (positive/negative) words for justices
#  8)  whether lawyers use all of their time ("reserve the remainder...")
#  9)  sentiment
#  10) how many times lawyers say "Your honor"
#  11) how many times justices interrupt each other
#  12) how many questions lawyers ask justices
#  13) how many pauses lawyers take
#  14) how many pauses justices take
#  15) how many times lawyers say "constitution"
#  16) how many times justices say "constitution"
#  17) whether an amicus curiae speaks
#  18) which side the amicus curiae speaks for
#  19) which justice speaks the most
#  20) how much the Chief Justice speaks


# 0) Get the names of the lawyers for the petitioners
#    and respondents.
# 1) Go through each line of the file and extract
#    features.

def extract_features(filename):
    """Extract features from a whitelist text file.
    Each whitelist text file has the same structure:

    Line 1: The list of petitioner lawyers.
    Line 2: The list of respodnent lawyers.
    Line 3: This line is always blank.

    The rest of lines are the text of the arguments,
    including bits of text that indicate a new speaker,
    such as:
    ORAL ARGUMENT OF...
    or
    REBUTTAL ARGUMENT OF...
    """
    with open(filename) as f:
        petitioner_line = f.readline().replace('\n', '')
        petitioners = petitioner_line.split(':')[1].split(',')

        respondent_line = f.readline().replace('\n', '')
        respondents = respondent_line.split(':')[1].split(',')

        # The third line of the file is always blank to make
        # visual inspection easier.
        f.readline()

        found_petitioner_argument_section = False
        found_respondent_argument_section = False

        found_lawyer_speech = False
        found_justice_speech = False

        # These are the features to extract.
        # Here are some brief descriptions:
        #
        # p_interruptions : The number of times petitioners are interrupted.
        # p_word_count    : The number of words petitioners speak.
        # p_laughter      : The number of times laughter occurs during the
        #                   petitioners section
        # p_num_justices  : The number of justices that speak to petitioners.
        # p_justice_word_count : The number of words justices speak to 
        #                        petitioners.
        # p_justice_interruptions : The number of times justices interrupt
        #                           each other during the petitioners' argument.
        # p_pauses        : The number of pauses petitioners take.
        # p_justice_pauses : The number of pauses justices take during
        #                    petitioners' argument.
        p_interruptions = 0
        r_interruptions = 0

        for line in f:
            # Determine which section of the text we are in:
            # petitioners' argument
            # OR
            # respondents' argument
            if line.startswith('ORAL ARGUMENT OF') or \
               line.startswith('REBUTTAL ARGUMENT OF'):
                if any(s in line for s in petitioners):
                    found_petitioner_argument_section = True
                    found_respondent_argument_section = False

                if any(s in line for s in respondents):
                    found_petitioner_argument_section = False
                    found_respondent_argument_section = True

            # Determine the type of speaker
            # lawyer
            # OR
            # justice
            if line.startswith('MR') or \
               line.startswith('MS') or \
               line.startswith('GENERAL'):
                found_lawyer_speech = True
                found_justice_speech = False

            if line.startswith('JUSTICE') or \
               line.startswith('CHIEF JUSTICE'):
                found_lawyer_speech = False
                found_justice_speech = True

            if found_petitioner_argument_section:
                if found_lawyer_speech:
                    p_interruptions += get_interruption(line)

                if found_justice_speech:
                    pass

            if found_respondent_argument_section:
                if found_lawyer_speech:
                    r_interruptions += get_interruption(line)

                if found_justice_speech:
                    pass

    return p_interruptions, r_interruptions

def get_interruption(line):
    return line.endswith('--\n')



if __name__ == '__main__':
    filename = '../txts_whitelist/02-1672.txt'
    p_interruptions, r_interruptions = extract_features(filename)

    print 'PETITIONER INTERRUPTIONS:'
    print p_interruptions
    print 'RESPONDENT INTERRUPTIONS:'
    print r_interruptions














