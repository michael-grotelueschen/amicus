import re


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
    reg = re.compile(r"""(?P<text>CHIEF.+|JUSTICE.+)
                      """, flags=re.MULTILINE|re.DOTALL|re.VERBOSE)
    with open(filename) as f:
        result = reg.search(f.read())
    return result

def reformat_text(text):
    """Reformat text so each speaker is on a separate line
    and so each ORAL ARGUMENT OF... text is on a separate line.
    """
    output_text = ''
    for line in text.split('\n')[:100]:
        if line.startswith('CHIEF') or \
           line.startswith('JUSTICE') or \
           line.startswith('MR') or \
           line.startswith('MS') or \
           line.startswith('GENERAL') or \
           line.startswith('ORAL ARGUMENT OF'):
           output_text += '\n'
        output_text += line
    return output_text
        




if __name__ == "__main__":
    filename = '../txts_clean/04-52.txt'
    ps, rs = get_speaker_names(filename)

    reg_obj = get_text_from_argument_section(filename)
    text = reg_obj.group('text')
    
    reformatted_text = reformat_text(text)
    print reformatted_text




# beginnings of speech:
# JUSTICE
# CHIEF
# MR.
# MS.
# GENERAL
#
#
# ends of speech:
# JUSTICE
# CHIEF
# MR.
# MS.
# GENERAL
# ORAL ARGUMENT OF
# \Z (This matches only at the end of the string)
# 
# 
# beginning of "ORAL ARGUMENT OF...":
# ORAL ARGUMENT OF
# 
# END OF "ORAL ARGUMENT OF..."
# MR.
# MS.
# JUSTICE
# CHIEF

# 0) Get the names of petitioners and respondents
#    (I should probably include these in the whitelist
#     text files for reference.)
# 
# 1) Get all of the text from the argument section
#    of the transcript.
# 
# 2) Divide up the remaining text into sections:
#    - justices
#    - laywers
#    - "ORAL ARGUMENT OF..."

