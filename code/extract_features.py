import pandas as pd
import numpy as np

def extract_transcript_features(filename):
    """Extract transcript features from a whitelist text file.
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
        # These are the transcript features to extract, with brief descriptions:
        # 
        # num_petitioner_lawyers : The number of lawyers arguing for the 
        #                          petitioners.
        # num_respondent_lawyers : The number of lawyers arguing for the 
        #                          respondents.
        # amicus_curiae : Whether an amicus curiae speaks.
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
            # petitioners' argument OR respondents' argument
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
            # Determine the type of speaker: lawyer OR justice
            if line.startswith('MR') or \
               line.startswith('MS') or \
               line.startswith('GENERAL'):
                found_lawyer_speech = True
                found_justice_speech = False
            else:
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

    amicus_curiae = int(amicus_curiae)
    p_rebuttal = int(p_rebuttal)
    p_num_justices = len(p_justice_set)
    r_num_justices = len(r_justice_set)

    features = [num_petitioner_lawyers, 
                num_respondent_lawyers, 
                amicus_curiae,

                p_interruption_count,
                p_word_count,
                p_laughter,
                p_pauses,
                p_question_count,
                p_your_honor_count,
                p_yes_count,
                p_no_count,
                p_I_count,
                p_rebuttal,
                p_case_reference_count,

                p_justice_word_count,
                p_justice_interruption_count,
                p_justice_pauses,
                p_justice_laughter,
                p_justice_question_count,
                p_chief_justice_count,
                p_justice_yes_count,
                p_justice_no_count,
                p_justice_I_count,
                p_justice_why_count,
                p_justice_case_reference_count,

                r_interruption_count,
                r_word_count,
                r_laughter,
                r_pauses,
                r_question_count,
                r_your_honor_count,
                r_yes_count,
                r_no_count,
                r_I_count,
                r_case_reference_count,

                r_justice_word_count,
                r_justice_interruption_count,
                r_justice_pauses,
                r_justice_laughter,
                r_justice_question_count,
                r_chief_justice_count,
                r_justice_yes_count,
                r_justice_no_count,
                r_justice_I_count,
                r_justice_why_count,
                r_justice_case_reference_count,

                p_num_justices,
                r_num_justices]
    return features

def get_transcript_feature_names():
    """Get a list of transcript feature names."""
    feature_names = ['num_petitioner_lawyers', 
                     'num_respondent_lawyers', 
                     'amicus_curiae',

                     'p_interruption_count',
                     'p_word_count',
                     'p_laughter',
                     'p_pauses',
                     'p_question_count',
                     'p_your_honor_count',
                     'p_yes_count',
                     'p_no_count',
                     'p_I_count',
                     'p_rebuttal',
                     'p_case_reference_count',

                     'p_justice_word_count',
                     'p_justice_interruption_count',
                     'p_justice_pauses',
                     'p_justice_laughter',
                     'p_justice_question_count',
                     'p_chief_justice_count',
                     'p_justice_yes_count',
                     'p_justice_no_count',
                     'p_justice_I_count',
                     'p_justice_why_count',
                     'p_justice_case_reference_count',

                     'r_interruption_count',
                     'r_word_count',
                     'r_laughter',
                     'r_pauses',
                     'r_question_count',
                     'r_your_honor_count',
                     'r_yes_count',
                     'r_no_count',
                     'r_I_count',
                     'r_case_reference_count',

                     'r_justice_word_count',
                     'r_justice_interruption_count',
                     'r_justice_pauses',
                     'r_justice_laughter',
                     'r_justice_question_count',
                     'r_chief_justice_count',
                     'r_justice_yes_count',
                     'r_justice_no_count',
                     'r_justice_I_count',
                     'r_justice_why_count',
                     'r_justice_case_reference_count',

                     'p_num_justices',
                     'r_num_justices']
    return feature_names

def get_scdb_feature_names():
    """Get a list of Supreme Court database feature names."""
    feature_names = ['argument_month']
    return []

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

def get_dockets():
    """Get all of the dockets to investigate."""
    filename = 'ok_cases'
    with open(filename) as f:
        dockets = [line.split('.')[0] for line in f if '.txt' in line]
    return dockets

def get_decisions(dockets):
    """Get the decisions for a set of dockets.
    Return a dictionary with dockets as keys and decicions as values.
    The decicions are either 1 (petitioner won) or 0 (respondent won).
    """
    # Use SCDB_2015_01_caseCentered_Citation.csv
    # Docket column is: 'docket'
    # Decision column is: 'partyWinning'
    # 'partyWinning' = 1: petitioner won
    # 'partyWinning' = 0: respondent won
    df_scdb = pd.read_csv('../scdb/SCDB_2015_01_caseCentered_Citation.csv')
    decisions = {}
    for docket in dockets:
        decision = df_scdb[df_scdb['docket']==docket]['partyWinning'].values[0]
        decisions[docket] = decision
    return decisions

def get_scdb_dataframe(dockets):
    """Get a Supreme Court Database dataframe that only includes the dockets
    we are interested in.
    """
    df_scdb = pd.read_csv('../scdb/SCDB_2015_01_caseCentered_Citation.csv')
    mask = [True if d in dockets else False for d in df_scdb['docket'].tolist()]
    df_scdb_subset = df_scdb[mask]
    # Enter a missing dateArgument for:
    # Docket 06-984: the correct date is Oct 10 2007
    # Docket 08-7621: the correct date is Nov 9 2009
    problem_case_1 = '06-984'
    correct_date_1 = '10/10/2007'
    problem_case_2 = '08-7621'
    correct_date_2 = '11/9/2009'
    df_scdb_subset.loc[df_scdb_subset['docket']==problem_case_1, 'dateArgument'] = correct_date_1
    df_scdb_subset.loc[df_scdb_subset['docket']==problem_case_2, 'dateArgument'] = correct_date_2

    df_scdb_subset['argument_month'] = df_scdb_subset['dateArgument'].apply(lambda d: int(d.split('/')[0]))

    x = df_scdb_subset[['docket', 'argument_month']]
    x = pd.concat([x, pd.get_dummies(df_scdb_subset['certReason'])], axis=1)
    x = pd.concat([x, pd.get_dummies(df_scdb_subset['naturalCourt'])], axis=1)
    x = pd.concat([x, pd.get_dummies(df_scdb_subset['chief'])], axis=1)
    x = pd.concat([x, pd.get_dummies(df_scdb_subset['issueArea'])], axis=1)
    x = pd.concat([x, pd.get_dummies(df_scdb_subset['jurisdiction'])], axis=1)
    return x

def extract_scdb_features(scdb_dataframe, docket):
    """Extract Supreme Court Database features for a particular docket.
    """
    row = scdb_dataframe[scdb_dataframe['docket']==docket].drop('docket', axis=1)
    features = row.values[0].tolist()
    return []

if __name__ == '__main__':

    output = 'docket,'
    feature_names = get_transcript_feature_names() + get_scdb_feature_names()
    output += ','.join(feature_names)
    output += ',decision\n'

    dockets = get_dockets()
    decisions = get_decisions(dockets)
    df_scdb = get_scdb_dataframe(dockets)

    for docket in dockets:
        filename = '../txts_whitelist/' + docket + '.txt'
        transcript_features = extract_transcript_features(filename)
        scdb_features = extract_scdb_features(df_scdb, docket)
        features = transcript_features + scdb_features

        output += docket + ','
        output += ','.join([str(f) for f in features]) + ','
        output += str(decisions[docket]) + '\n'

with open('test_feature_matrix.csv', 'w') as f:
        f.write(output)