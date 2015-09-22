import requests
import urlparse
import os

from bs4 import BeautifulSoup

def get_pdf_urls():
    """Scrape the Supreme Court oral argument transcript sites
    to return a list of urls to all of the oral argument transcript pdfs.

    The site urls look like this:
    http://www.supremecourt.gov/oral_arguments/argument_transcript/[YEAR]
    where [YEAR] starts at 2004 and ends at 2014

    The pdf urls look like this:
    http://www.supremecourt.gov/oral_arguments/argument_transcripts/[NAME].pdf
    """
    prefix = "http://www.supremecourt.gov/oral_arguments/argument_transcript/"
    base_urls = [prefix + str(num) for num in range(2004, 2015)]
    pdf_urls = []

    for base_url in base_urls:
        l = requests.get(base_url)
        soup = BeautifulSoup(l.content, 'html.parser')

        # Find every oral argument transcript url ('href') in the html.
        for a in soup.find_all('a', href=True):
            if a['href'].startswith('../argument_transcripts/'):
                pdf_url = urlparse.urljoin(base_url, a['href'])
                pdf_urls.append(pdf_url)

    return pdf_urls

def download_pdfs(pdf_urls):
    """Download each oral argument transcript pdf."""
    for pdf_url in pdf_urls:
        os.system('wget %s' % pdf_url)

if __name__ == '__main__':
    pdf_urls = get_pdf_urls()
    download_pdfs(pdf_urls)