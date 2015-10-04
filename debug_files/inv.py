import os
import re
import pandas as pd




def get_speaker_amiguity(filename):
    """Get full speaker names for both petitioners and respondents."""
    petitioner_strings = ['petitioner',\
                          'appellant',\
                          'plaintiff']
    respondent_strings = ['respondent',\
                          'appellee',\
                          'defendant']
    # The second 'start' condition is for case 10-7387,
    # which does not include the word 'APPEARANCES'
    reg = re.compile(r"""(?P<start>APPEARANCES:\n|
                                   JASON\sD\.\sHAWKINS,\sESQ\.,\sAssistant\sFederal\sPublic)
                         (?P<speakers>.+?)
                         (?P<end>\nC\sO\sN\sT\sE\sN\sT\sS|
                                 \nC\sO\sIn\sT\sE\sIn\sT\sS|
                                 \nORAL\sARGUMENT\sOF\sPAGE)
                      """, flags=re.MULTILINE|re.DOTALL|re.VERBOSE)

    with open(filename) as f:
        match = reg.search(f.read())
    # This is to account for the 'start' condition for case 10-7387
    if 'JASON D. HAWKINS' in match.group('start'):
        speakers_string = match.group('start') + match.group('speakers')
    else:
        speakers_string = match.group('speakers')

    any_speaker_ambiguity = False
    speakers = speakers_string.split('.\n')
    for speaker in speakers:
        name = speaker.split(',')[0]
        if any(s in speaker.lower() for s in petitioner_strings) and \
           any(s in speaker.lower() for s in respondent_strings) and \
           'neither' not in speaker.lower():
            any_speaker_ambiguity = True

        if 'neither' in speaker.lower():
            any_speaker_ambiguity = True

        if not any(s in speaker.lower() for s in petitioner_strings) and \
           not any(s in speaker.lower() for s in respondent_strings) and \
           'neither' not in speaker.lower():
            any_speaker_ambiguity = True

    return any_speaker_ambiguity





if __name__ == "__main__":
    ambiguous_files = []
    for filename in os.listdir('../txts_clean/'):
        full_filename = '../txts_clean/' + filename
        speaker_ambiguity = get_speaker_amiguity(full_filename)
        if speaker_ambiguity:
            ambiguous_files.append(filename)

    df = pd.read_csv('../scdb/SCDB_2015_01_caseCentered_Citation.csv')
    dockets = df['docket'].tolist()
    cases_not_in_scdb = []
    for filename in os.listdir('../txts_clean/'):
        #full_filename = '../txts_clean/' + filename
        case = filename.replace('.txt', '')
        if case not in dockets:
            cases_not_in_scdb.append(filename)

    cases_to_ignore = ambiguous_files + cases_not_in_scdb
    ok_cases = []
    for filename in os.listdir('../txts_clean/'):
        if filename not in cases_to_ignore:
            ok_cases.append(filename)

    print '\n'.join(ok_cases)
    print len(ok_cases)

    with open('ok_cases', 'w') as f:
        f.write('\n'.join(ok_cases))