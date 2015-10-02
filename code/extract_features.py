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
        petitioner_line = f.readline()
        respondent_line = f.readline()
        # The third line of the file is always blank
        f.readline()

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
        # 

if __name__ == '__main__':














