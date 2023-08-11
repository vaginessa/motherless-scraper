# Motherless Scraper
A motherless.com scraper to download all videos and images from a search query.

# Usage
`python3 ./scrape.py <term> <download_dir>`
* `term` - Search term to query.
* `download_dir` - Destination directory for the media to be saved to.

# Requirements
In its current state, this scraper requires: requests and bs4.

You can install these requirements by using:

`python3 -m pip install -r requirements.txt`

For more information on the individual requirements and how to install them manually, see below.

### Requests
`python3 -m pip install requests`

This is required to send the network requests to query the target website and download the media.

### bs4
`python3 -m pip install bs4`

This is required to parse the webpage more easily.

# A Note on Scraping
It is entirely possible that this will not work in the future. Web scraping is fragile. If the layout of the webpage changes, then any scraping tool may parse the new page incorrectly. This version is confirmed to work as of August 11, 2023. If you encounter any problems after this date, please open an issue.
