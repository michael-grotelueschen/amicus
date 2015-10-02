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
        # p_pauses        : The number of pauses petitioners take.
        # p_question_count : The number of questions petitioners ask.
        # 
        # p_num_justices  : The number of justices that speak to petitioners.
        # p_justice_word_count : The number of words justices speak to 
        #                        petitioners.
        # p_justice_interruptions : The number of times justices are 
        #                           interrupted during the petitioners' argument.
        # p_justice_pauses : The number of pauses justices take during
        #                    petitioners' argument.
        # p_justice_laughter : The number of times laughter occurs during
        #                      a justices speech.
        # p_justice_question_count : The number of questions justices ask
        #                            during the petitioners' argument.
        # 
        # 

        p_interruption_count = 0
        p_word_count = 0
        p_laughter = 0
        p_pauses = 0
        p_question_count = 0

        p_justice_word_count = 0
        p_justice_interruption_count = 0
        p_justice_pauses = 0
        p_justice_laughter = 0
        p_justice_set = set([])
        p_justice_question_count = 0

        r_interruption_count = 0
        r_word_count = 0
        r_laughter = 0
        r_pauses = 0
        r_question_count = 0

        r_justice_word_count = 0
        r_justice_interruption_count = 0
        r_justice_pauses = 0
        r_justice_laughter = 0
        r_justice_set = set([])
        r_justice_question_count = 0

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
                continue

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
                    p_interruption_count += get_interruption(line)
                    p_word_count += get_word_count(line)
                    p_pauses += get_pauses(line)
                    p_laughter += get_laughter(line)
                    p_question_count += get_question_count(line)

                if found_justice_speech:
                    p_justice_word_count += get_word_count(line)
                    p_justice_interruption_count += get_interruption(line)
                    p_justice_pauses += get_pauses(line)
                    p_justice_laughter += get_laughter(line)

                    justice_name = [get_justice_name(line)]
                    p_justice_set.update(justice_name)
                    p_justice_question_count += get_question_count(line)

            if found_respondent_argument_section:
                if found_lawyer_speech:
                    r_interruption_count += get_interruption(line)
                    r_word_count += get_word_count(line)
                    r_pauses += get_pauses(line)
                    r_laughter += get_laughter(line)
                    r_question_count += get_question_count(line)

                if found_justice_speech:
                    r_justice_word_count += get_word_count(line)
                    r_justice_interruption_count += get_interruption(line)
                    r_justice_pauses += get_pauses(line)
                    r_justice_laughter += get_laughter(line)

                    justice_name = [get_justice_name(line)]
                    r_justice_set.update(justice_name)
                    r_justice_question_count += get_question_count(line)


    p_num_justices = len(p_justice_set)
    r_num_justices = len(r_justice_set)

    print 'PETITIONER:'
    print p_justice_question_count
    print 
    print 'RESPONDENT:'
    print r_justice_question_count

def get_interruption(line):
    return line.endswith('--\n')

def get_word_count(line):
    """Get the word count of a line, but ignore 'CHIEF JUSTICE'
    and 'JUSTICE' and '[NAME]:'
    """
    if line.startswith('CHIEF'):
        return len(line.split(' ')) - 3
    else:
        return len(line.split(' ')) - 2        

def get_laughter(line):
    return '(Laughter.)' in line

def get_pauses(line):
    return line.count(' -- ')

def get_justice_name(line):
    name_string = line.split(':')[0]
    name = name_string.split(' ')[-1]
    return name

def get_question_count(line):
    return line.count('?')


if __name__ == '__main__':
    filename = '../txts_whitelist/02-1672.txt'
    extract_features(filename)











