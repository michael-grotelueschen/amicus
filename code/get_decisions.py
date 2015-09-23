import os
import re
import pandas as pd

def get_dockets():
    """Get all of the dockets to investigate."""
    filename = '../debug_files/ok_case_names'
    with open(filename) as f:
        dockets = [line.split('.')[0] for line in f if '.txt' in line]
    return dockets

def get_dockets_and_decisions():
    """Get the decisions for all of the dockets.
    Return a dictionary with dockets as keys and decicions as values.
    The decicions are either 1 (petitioner won) or 0 (respondent won).
    """
    dockets = get_dockets()
    df = pd.read_csv('../scdb/SCDB_2015_01_caseCentered_Citation.csv')    

    dockets_and_decisions = {}
    for docket in dockets:
        decision = df[df['docket'] == docket]['partyWinning'].values[0]
        dockets_and_decisions[docket] = decision
    return dockets_and_decisions

def get_speaker_names(filename):
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
    full_filename = '../txts_clean/' + filename
    with open(full_filename) as f:
        match = reg.search(f.read())
    # This is to account for the 'start' condition for case 10-7387
    if 'JASON D. HAWKINS' in match.group('start'):
        speakers_string = match.group('start') + match.group('speakers')
    else:
        speakers_string = match.group('speakers')

    speakers = speakers_string.split('.\n')
    petitioner_speakers = []
    respondent_speakers = []
    for speaker in speakers:
        name = speaker.split(',')[0]
        if any(s in speaker.lower() for s in petitioner_strings):
            petitioner_speakers.append(name)
        else:
            respondent_speakers.append(name)
    return petitioner_speakers, respondent_speakers

def get_interruption_count():
    """Get the interruption counts for both petitioners
    and respondents.
    """
    petitioner_interruption_count = 0
    respondent_interruption_count = 0

    petitioners = ['WILLIAM W. LOCKYER']
    respondents = ['MARK R. DROZDOWSKI']

    filename = '../txts_clean/04-52.txt'
    for petitioner in petitioners:
        last_name = petitioner.split(' ')[-1]
        count = get_individual_interruption_count(filename, last_name)
        petitioner_interruption_count += count

    for respondent in respondents:
        last_name = respondent.split(' ')[-1]
        count = get_individual_interruption_count(filename, last_name)
        respondent_interruption_count += count        

    return petitioner_interruption_count, respondent_interruption_count
      
def get_individual_interruption_count(filename, last_name):
    """Get the interruption count for an individual speaker."""
    interruption_count = 0
    reg = re.compile(r"""(?P<start>\s{last_name}:\s)
                         (?P<speech>.+?)
                         (?P<end>\nJUSTICE|\nCHIEF)
                      """.format(last_name=last_name), \
                         flags=re.MULTILINE|re.DOTALL|re.VERBOSE)

    with open(filename) as f:
        for result in reg.finditer(f.read()):
            speech = result.groupdict()['speech']
            if speech.endswith('--'):
                interruption_count += 1
    
    return interruption_count


if __name__ == '__main__':
    get_interruption_count()






