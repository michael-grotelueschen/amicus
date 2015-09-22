import os
import re

def get_speaker_names():
    """Get the names of speakers and determine
    which side they represent.
    """

    # The second 'start' condition is for case 10-7387,
    # which does not include the word 'APPEARANCES'
    reg = re.compile(r"""(?P<start>APPEARANCES:\n|
                                   JASON\sD\.\sHAWKINS,\sESQ\.,\sAssistant\sFederal\sPublic)
                         (?P<speakers>.+?)
                         (?P<end>\nC\sO\sN\sT\sE\sN\sT\sS|
                                 \nC\sO\sIn\sT\sE\sIn\sT\sS|
                                 \nORAL\sARGUMENT\sOF\sPAGE)
                      """, flags=re.MULTILINE|re.DOTALL|re.VERBOSE)

    """
    supporting affirmance

    supporting affirmance in part and vacatur in part

    in support of neither party
    in support of neitherparty
    supporting neither party

    supporting partial reversal

    supporting the Respondents in 03-1238 and thePetitioners in 04-66.

    amicus curiae

    MALCOLM L. STEWART, ESQ., Assistant to the Solicitor
    General, Department of Justice, Washington, D.C.; on
    behalf of the United States, as amicus curiae,
    supporting the Respondents in No. 03-1230 and
    supporting the Petitioners in No. 03-1234.
    """
    petitioner_strings = ['petitioner',\
                          'appellant',\
                          'plaintiff']

    respondent_strings = ['respondent',\
                          'appellee',\
                          'defendant']
                          
    output1 = ''
    output2 = ''
    output3 = ''
    output4 = ''
    for filename in os.listdir('txts_clean/'):
        full_filename = 'txts_clean/' + filename
        with open(full_filename) as f:
            match = reg.search(f.read())

            # This is to account for the 'start' condition for case 10-7387
            if 'JASON D. HAWKINS' in match.group('start'):
                speakers_string = match.group('start') + match.group('speakers')
            else:
                speakers_string = match.group('speakers')

            speakers = speakers_string.split('.\n')
            for speaker in speakers:
                found_petitioner = any(s in speaker.lower() for s in petitioner_strings)
                found_respondent = any(s in speaker.lower() for s in respondent_strings)

                if not found_petitioner and not found_respondent:
                    output1 += filename + ' : ' + speaker.replace('\n', ' ') + '\n'

                if found_petitioner and not found_respondent:
                    output2 += filename + ' : ' + speaker.replace('\n', ' ') + '\n'

                if not found_petitioner and found_respondent:
                    output3 += filename + ' : ' + speaker.replace('\n', ' ') + '\n'

                if found_petitioner and found_respondent:
                    output4 += filename + ' : ' + speaker.replace('\n', ' ') + '\n'

    with open('reg_ex_test__1', 'w') as f:
        f.write(output1)

    with open('reg_ex_test__2', 'w') as f:
        f.write(output2)

    with open('reg_ex_test__3', 'w') as f:
        f.write(output3)

    with open('reg_ex_test__4', 'w') as f:
        f.write(output4)

def list_problems():
    output = set([])
    for filename in os.listdir('txts_clean/'):
        full_filename = 'txts_clean/' + filename

        with open(full_filename) as f:
            for line in f.readlines():
                if line.startswith('Page'):
                    output.add(filename)
    print '\n'.join(output)

if __name__ == '__main__':
    list_problems()