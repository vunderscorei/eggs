# EGGS: Emergency Google Groups Scraper *(work in progress)*

Google Groups Usenet newsgroup backup utility written in Python with Pydoll Loosely based on Justin Parnell's [Google Groups Scraper](https://github.com/parnellj/google_groups_scraper). Not fully functional yet.

## Requirements:

- Python 3.13 or newer
- Google Chrome

## Usage:

Clone the project, and navigate to the project's root. Run `python3 src/launch.py --newsgroup <group> --metadata-out <dir>` where <group> is the newsgroup you wish to scrape, and <dir> is an output directory. On windows, replace the first part of the command with `python src\launch.py`. This will generate a file with metadata (but not the body) of every post in the selected newsgroup.

Ideally, this should be a single run that gathers all posts. While you can technically resume at a later point, it's usually not worth it. Currently, due to the way paging and works in Google Groups, it will take almost as long to jump to a later page as it would to just start over from scratch. GGScraper can process roughly 9,000 posts an hour, but this will vary based on any number of factors.

Currently, this is as far as EGGS can go. Work on using this metadata to download the posts' content and format it into an MBOX is ongoing.

## Caveats:

- The program flat out isn't done yet, and can only retrieve post metadata at the moment.
- EGGS only works with Google Chrome, due to rendering issues with the Google Groups site in other browsers.
- EGGS only implements the barest of anti-anti-scraper mechanisms (mostly just by being really slow), and there is a low chance Google may rate limit or even temporarily block your IP. A VPN or proxy is recommended if you plan on running EGGS for extended periods of time or on multiple machines simultaneously.
- The web scraping relies on a number of hard-coded values pointing to tags with randomly generated descriptors. If Google changes anything about how the Groups site is rendered, this will almost certainly break.
- I know *very* little python, and the quality of the code reflects this.
