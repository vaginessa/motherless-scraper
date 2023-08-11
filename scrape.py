from sys import stdout, argv
from scraping_utils.scraping_utils import compute_file_hashes, download_urls
from bs4 import BeautifulSoup
import requests, time, os, re


"""
Convert a URL string to a BeautifulSoup.
@param url - URL to convert.
"""
def to_bs(url):
    try:
        res = requests.get(url)
        return BeautifulSoup(res.content, 'html.parser')
    except:
        return None


"""
Download from the images tab.
@param url - Base url to download from.
@dst - Directory to download to.
@hashes - Hashes of existing downloads
"""
def process_images(url, dst, hashes):
    # Get the main page
    page = to_bs(url)
    if(page is None):
        stdout.write(f'[process_images] INFO: Failed to fetch from {url}.\n')
        return

    # Get the number of pages
    try: pages = int(page.find(class_='content-wrapper').findAll(class_='pop')[-2].text)
    except: pages = 1
    if(pages != 1): pages = pages + 1

    # Iterate the pages
    downloads = []
    for i in range(1, pages):
        stdout.write(f'[process_images] INFO: Loading page {i}/{pages-1}...\n')
        page_url = url + f'?page={i}'
        page_page = to_bs(page_url)
        if(page_page is None):
            stdout.write(f'[process_images] INFO: Failed to fetch from {page_url}\n')
            continue

        thumbs = page_page.find(class_='content-inner').findAll(class_='img-container')
        for thumb in thumbs:
            img_id = thumb['href'].split('/')[-1]
            ext = thumb.find(class_='static')['src'][-3:]
            downloads.append(f'http://cdn5-images.motherlessmedia.com/images/{img_id}.{ext}')
            stdout.write(f'[process_images] INFO: Found image: {downloads[-1]}\n')

    # Download every found image
    stdout.write('[process_videos] INFO: Beginning image downloads...\n')
    download_urls(dst, downloads, hashes=hashes)
    return



"""
Download from the videos tab.
@param url - Base url to download from.
@param dst - Directory to download to.
@param hashes - Hashes of existing downloads.
"""
def process_videos(url, dst, hashes={}):
    # Get the main page
    page = to_bs(url)
    if(page is None):
        stdout.write(f'[process_videos] INFO: Failed to fetch from {url}.\n')
        return

    # Get the number of pages
    try: pages = int(page.find(class_='content-wrapper').findAll(class_='pop')[-2].text)
    except: pages = 1
    if(pages != 1): pages = pages + 1

    # Iterate the pages
    downloads = []
    for i in range(1, pages):
        stdout.write(f'[process_videos] INFO: Loading page {i}/{pages-1}...\n')
        page_url = url + f'?page={i}'
        page_page = to_bs(page_url)
        if(page_page is None):
            stdout.write(f'[process_videos] INFO: Failed to fetch from {page_url}\n')
            continue

        thumbs = page_page.find(class_='content-inner').findAll(class_='img-container')
        for thumb in thumbs:
            vid_url = thumb['href']
            vid_page = to_bs(vid_url)
            if(vid_page is None):
                stdout.write(f'[process_videos] INFO: Failed to fetch from {vid_url}.\n')
                continue
            source = vid_page.find('source')
            if(source is not None):
                downloads.append(source['src'].replace('https', 'http'))
                stdout.write(f'[process_videos] INFO: Found video: {downloads[-1]}\n')

    # Download every found video
    stdout.write('[process_videos] INFO: Beginning video downloads...\n')
    download_urls(dst, downloads, hashes=hashes)
    return


"""
Driver function to scrape a motherless term.
@param term - Term to scrape.
@param dst - Destination directory to store the downloads.
"""
def main(term, dst):
    # Create the base URLs
    vid_url = 'https://motherless.com/term/videos/' + term
    img_url = 'https://motherless.com/term/images/' + term

    # Compute the hashes
    stdout.write('[main] Computing video hashes...\n')
    vid_hashes = compute_file_hashes(os.path.join(dst, 'vids'))
    stdout.write('[main] Computing image hashes...\n')
    pic_hashes = compute_file_hashes(os.path.join(dst, 'pics'))

    process_videos(vid_url, os.path.join(dst, 'vids'), hashes=vid_hashes)
    process_images(img_url, os.path.join(dst, 'pics'), hashes=pic_hashes)


"""
Entry point
"""
if(__name__ == '__main__'):
    stdout.write('\n')
    if(len(argv) != 3):
        stdout.write(f'USAGE: {argv[0]} <term> <download_dir>\n')
    else:
        if(not os.path.isdir(argv[2])):
            os.mkdir(argv[2])
        if(not os.path.isdir(os.path.join(argv[2], 'vids'))):
            os.mkdir(os.path.join(argv[2], 'vids'))
        if(not os.path.isdir(os.path.join(argv[2], 'pics'))):
            os.mkdir(os.path.join(argv[2], 'pics'))
        main(argv[1], argv[2])
    stdout.write('\n')
