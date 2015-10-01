import re

def get_dockets():
    """Get all of the dockets to investigate."""
    filename = '../debug_files/ok_case_names'
    with open(filename) as f:
        dockets = [line.split('.')[0] for line in f if '.txt' in line]
    return dockets

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

def get_text_from_argument_section(filename):
    """Get all of the text from the argument section of the transcript."""

    # The last two conditions for the end of the regular expression are for:
    #     case 14556 part 1   : '(Short break at 11:32 a.m.)'
    #     case 03-1693        : 'now adjourned until Monday next at 10'
    reg = re.compile(r"""(?P<text>CHIEF.+|
                                  JUSTICE.+)
                         (?P<end>\(Wher|
                                 \[Wher|
                                 \[\sWher|
                                 Whereupon,|
                                 \(Short\sbreak\sat\s11:32\sa\.m\.|
                                 now\sadjourned\suntil\sMonday\snext\sat\s10)
                      """, flags=re.MULTILINE|re.DOTALL|re.VERBOSE)
    with open(filename) as f:
        result = reg.search(f.read())
    return result

def reformat_text(filename):
    """Reformat text so each speaker is on a separate line
    and so each example of "ORAL ARGUMENT OF..." text is on a separate line.

    The purpose of this format is to avoid needing regular expressions
    to extract features.
    """
    petitioner_speakers, respondent_speakers = get_speaker_names(filename)
    output_text  = 'PETITIONERS:' + ','.join(petitioner_speakers) + '\n'
    output_text += 'RESPONDENTS:' + ','.join(respondent_speakers) + '\n\n'

    reg_obj = get_text_from_argument_section(filename)
    text = reg_obj.group('text')

    beginning_of_text = True
    for line in text.split('\n'):
        if line.startswith('CHIEF') or \
           line.startswith('JUSTICE') or \
           line.startswith('MR') or \
           line.startswith('MS') or \
           line.startswith('GENERAL') or \
           line.startswith('ORAL ARGUMENT OF') or \
           line.startswith('REBUTTAL ARGUMENT OF'):

            if beginning_of_text:
                beginning_of_text = False
            else:
                output_text += '\n'

        else:
            output_text += ' '

        output_text += line
    return output_text
        

if __name__ == "__main__":
    dockets = get_dockets()
    for docket in dockets:
        filename = '../txts_clean/' + docket + '.txt'
        output_filename = filename.replace('../txts_clean', '../txts_whitelist')

        reformatted_text = reformat_text(filename)
        with open(output_filename, 'w') as f:
            f.write(reformatted_text)