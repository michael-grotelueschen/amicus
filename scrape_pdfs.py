import requests
import urlparse
import os

from bs4 import BeautifulSoup


# urls:
# 
# http://www.supremecourt.gov/oral_arguments/argument_transcript/2004
# ...
# http://www.supremecourt.gov/oral_arguments/argument_transcript/2014
#
# http://www.supremecourt.gov/oral_arguments/argument_transcript/2004
# http://www.supremecourt.gov/oral_arguments/argument_transcripts/04-603.pdf

def get_pdf_urls():
    prefix = "http://www.supremecourt.gov/oral_arguments/argument_transcript/"
    base_urls = [prefix + str(num) for num in range(2004, 2015)]
    pdf_urls = []

    for base_url in base_urls:
        l = requests.get(base_url)
        soup = BeautifulSoup(l.content, 'html.parser')
        for a in soup.find_all('a', href=True):
            #print "Found the URL:", a['href']
            if a['href'].startswith('../argument_transcripts/'):
                pdf_url = urlparse.urljoin(base_url, a['href'])
                pdf_urls.append(pdf_url)

    return pdf_urls

def download_pdfs(pdf_urls):
    for pdf_url in pdf_urls:
        os.system('wget %s' % pdf_url)


if __name__ == '__main__':
    pdf_urls = get_pdf_urls()
    download_pdfs(pdf_urls)