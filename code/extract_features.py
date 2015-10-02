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
        # num_petitioner_lawyers : The number of lawyers arguing for the 
        #                          petitioners.
        # num_respondent_lawyers : The number of lawyers arguing for the 
        #                          respondents.
        #
        # p_interruptions : The number of times petitioners are interrupted.
        # p_word_count    : The number of words petitioners speak.
        # p_laughter      : The number of times laughter occurs during the
        #                   petitioners section
        # p_pauses        : The number of pauses petitioners take.
        # p_question_count : The number of questions petitioners ask.
        # p_your_honor_count : The number of times petitioners say
        #                      'Your honor'
        # p_yes_count : The number of times petitioners say 'yes'.
        # p_no_count : The number of times petitioners say 'no'.
        # p_I_count : The number of times petitioners say 'I'.
        # p_rebuttal : Did the petitioner offer a rebuttal?
        # p_case_reference_count : The number of times a petitioner
        #                          references a case.
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
        # p_chief_justice_count : How many times the chief justice speaks
        #                         during the petitioners' argument.
        # p_justice_yes_count : The number of times justices say 'yes'.
        # p_justice_no_count : The number of times justices say 'no'.
        # p_justice_I_count : The number of times justices say 'I'.
        # p_justice_why_count : The number of times justices say 'why'.
        # p_justice_case_reference_count : The number of times justices reference
        #                                  cases.
        # 

        num_petitioner_lawyers = len(petitioners)
        num_respondent_lawyers = len(respondents)
        amicus_curiae = False

        p_interruption_count = 0
        p_word_count = 0
        p_laughter = 0
        p_pauses = 0
        p_question_count = 0
        p_your_honor_count = 0
        p_yes_count = 0
        p_no_count = 0
        p_I_count = 0
        p_rebuttal = False
        p_case_reference_count = 0

        p_justice_word_count = 0
        p_justice_interruption_count = 0
        p_justice_pauses = 0
        p_justice_laughter = 0
        p_justice_set = set([])
        p_justice_question_count = 0
        p_chief_justice_count = 0
        p_justice_yes_count = 0
        p_justice_no_count = 0
        p_justice_I_count = 0
        p_justice_why_count = 0
        p_justice_case_reference_count = 0

        r_interruption_count = 0
        r_word_count = 0
        r_laughter = 0
        r_pauses = 0
        r_question_count = 0
        r_your_honor_count = 0
        r_yes_count = 0
        r_no_count = 0
        r_I_count = 0
        r_case_reference_count = 0

        r_justice_word_count = 0
        r_justice_interruption_count = 0
        r_justice_pauses = 0
        r_justice_laughter = 0
        r_justice_set = set([])
        r_justice_question_count = 0
        r_chief_justice_count = 0
        r_justice_yes_count = 0
        r_justice_no_count = 0
        r_justice_I_count = 0
        r_justice_why_count = 0
        r_justice_case_reference_count = 0

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

                if line.startswith('REBUTTAL ARGUMENT OF'):
                    p_rebuttal = True

                if 'AMICUS' in line:
                    amicus_curiae = True
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
                    p_your_honor_count += get_your_honor_count(line)
                    p_yes_count += get_yes_count(line)
                    p_no_count += get_no_count(line)
                    p_I_count += get_I_count(line)
                    p_case_reference_count += get_case_reference_count(line)

                if found_justice_speech:
                    p_justice_word_count += get_word_count(line)
                    p_justice_interruption_count += get_interruption(line)
                    p_justice_pauses += get_pauses(line)
                    p_justice_laughter += get_laughter(line)

                    justice_name = [get_justice_name(line)]
                    p_justice_set.update(justice_name)
                    p_justice_question_count += get_question_count(line)
                    p_chief_justice_count += get_chief_justice_count(line)

                    p_justice_yes_count += get_yes_count(line)
                    p_justice_no_count += get_no_count(line)
                    p_justice_I_count += get_I_count(line)
                    p_justice_why_count += get_why_count(line)
                    p_justice_case_reference_count += get_case_reference_count(line)

            if found_respondent_argument_section:
                if found_lawyer_speech:
                    r_interruption_count += get_interruption(line)
                    r_word_count += get_word_count(line)
                    r_pauses += get_pauses(line)
                    r_laughter += get_laughter(line)
                    r_question_count += get_question_count(line)
                    r_your_honor_count += get_your_honor_count(line)
                    r_yes_count += get_yes_count(line)
                    r_no_count += get_no_count(line)
                    r_I_count += get_I_count(line)
                    r_case_reference_count += get_case_reference_count(line)

                if found_justice_speech:
                    r_justice_word_count += get_word_count(line)
                    r_justice_interruption_count += get_interruption(line)
                    r_justice_pauses += get_pauses(line)
                    r_justice_laughter += get_laughter(line)

                    justice_name = [get_justice_name(line)]
                    r_justice_set.update(justice_name)
                    r_justice_question_count += get_question_count(line)
                    r_chief_justice_count += get_chief_justice_count(line)

                    r_justice_yes_count += get_yes_count(line)
                    r_justice_no_count += get_no_count(line)
                    r_justice_I_count += get_I_count(line)
                    r_justice_why_count += get_why_count(line)
                    r_justice_case_reference_count += get_case_reference_count(line)


    p_num_justices = len(p_justice_set)
    r_num_justices = len(r_justice_set)

    print 'PETITIONER:'
    print p_justice_case_reference_count
    print 
    print 'RESPONDENT:'
    print r_justice_case_reference_count

def get_interruption(line):
    return line.endswith('--\n')

def get_word_count(line):
    """Get the word count of a line, but ignore 'CHIEF JUSTICE'
    and 'JUSTICE' and '[NAME]:'
    """
    word_count = len(line.split(' '))
    if line.startswith('CHIEF'):
        word_count -= 3
    else:
        word_count -= 2
    return word_count

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

def get_chief_justice_count(line):
    return line.startswith('CHIEF')

def get_your_honor_count(line):
    return line.lower().count('your honor')

def get_yes_count(line):
    return line.lower().count('yes')

def get_no_count(line):
    no_count =  line.lower().count(' no ')
    no_count += line.lower().count(' no.')
    no_count += line.lower().count(' no,')
    return no_count

def get_I_count(line):
    return line.count('I')

def get_why_count(line):
    return line.lower().count('why')

def get_case_reference_count(line):
    return line.count(' v. ')

if __name__ == '__main__':
    #filename = '../txts_whitelist/02-1672.txt'
    filename = '../txts_whitelist/03-10198.txt'
    extract_features(filename)











