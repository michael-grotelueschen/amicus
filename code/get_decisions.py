import os
import re
import pandas as pd

def get_dockets():
    """Get all of the dockets to investigate."""
    filename = '../debug_files/ok_case_names'
    with open(filename) as f:
        dockets = [line.split('.')[0] for line in f if '.txt' in line]
    return dockets

def get_decisions():
    """Get the decisions for all of the dockets.
    Return a dictionary with dockets as keys and decicions as values.
    The decicions are either 1 (petitioner won) or 0 (respondent won).
    """
    dockets = get_dockets()

    # Use SCDB_2015_01_caseCentered_Citation.csv
    # Docket column is: 'docket'
    # Decision column is: 'partyWinning'
    # 'partyWinning' = 1: petitioner won
    # 'partyWinning' = 0: respondent won
    df = pd.read_csv('../scdb/SCDB_2015_01_caseCentered_Citation.csv')    

    decisions = {}
    for docket in dockets:
        decision = df[df['docket'] == docket]['partyWinning'].values[0]
        decisions[docket] = decision
    return decisions

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

    with open(filename) as f:
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

def get_interruption_count(filename, petitioners, respondents):
    """Get the interruption counts for both petitioners
    and respondents.
    """
    petitioner_interruption_count = 0
    respondent_interruption_count = 0

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
    output = ''

    dockets = get_dockets()
    decisions = get_decisions()

    for docket in dockets:
        filename = '../txts_clean/' + docket + '.txt'
        petitioner_speakers, respondent_speakers = get_speaker_names(filename)

        petitioner_interruption_count, \
        respondent_interruption_count = get_interruption_count(filename,\
                                                               petitioner_speakers,\
                                                               respondent_speakers)

        output += docket + ','
        output += str(petitioner_interruption_count) + ','
        output += str(respondent_interruption_count) + ','
        output += str(decisions[docket]) + '\n'

    with open('test', 'w') as f:
        f.write(output)






