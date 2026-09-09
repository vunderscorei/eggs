import asyncio
import json
import os.path
import random
import re
import time
from datetime import datetime
from pathlib import Path

import lxml.html
from pydoll.browser import Chrome

from .directory_entry import DirectoryEntry
from .selectors import DIRECTORY_SELECTORS

HERE = Path(os.path.dirname(os.path.realpath(__file__)))

GOOGLE_GROUP_BASE = 'https://groups.google.com/g/'
SEARCH_URL = GOOGLE_GROUP_BASE + "{newsgroup}/search?q={params}"

# warning: '–' != '-'
PAGE_NUM_REGEX = r'(\d+)–(\d+)\sof\s(many|\d+)'


class DirectoryScraper:
    def __init__(self, newsgroup, after=None, before=None, author=None, subject=None, query=None):
        self.newsgroup = newsgroup
        self.after = after or datetime(1970, 1, 1)
        self.before = before or datetime.today()
        self.author = author
        self.subject = subject
        self.query = query
        self.start_page_num = 0
        self.current_page_num = 0
        self.directory_entries = set()
        self.search_url = self.generate_search_url()
        self.page = None

    def generate_search_url(self):
        params = 'after:%s before:%s' % (self.after.strftime('%Y-%m-%d'), self.before.strftime('%Y-%m-%d'))
        if self.author is not None:
            params += ' author:"%s"' % self.author
        if self.subject is not None:
            params += ' subject:"%s"' % self.subject
        if self.query is not None:
            params += ' "%s"' % self.query

        return SEARCH_URL.format(newsgroup=self.newsgroup, params=params)

    async def read_page(self, tab):
        source = await tab.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        self.page = lxml.html.fromstring(source['result']['result']['value'])

    def add_page_entries(self):
        entries = self.page.xpath(DIRECTORY_SELECTORS['entry'])
        for entry in entries:
            self.directory_entries.add(DirectoryEntry(self.newsgroup, entry))

    # returns (start_post_num, end_post_num, is_last_page)
    def parse_page_post_nums(self):
        raw_page_num = self.page.xpath(DIRECTORY_SELECTORS['page_num'])[0].text
        match = re.search(PAGE_NUM_REGEX, raw_page_num.strip())
        start = match.group(1)
        end = match.group(2)
        limit = match.group(3)
        return int(start), int(end), (end == limit)

    # returns True if there are more pages
    async def next_page(self, tab):
        start, end, is_last_page = self.parse_page_post_nums()
        print('Current page: (%d-%d)' % (start, end))
        if is_last_page:
            print('On last page!')
            return False
        else:
            print('Clicking "Next page"...')
            next_button = await tab.find(aria_label='Next page')
            await next_button.click()
            time.sleep(random.uniform(2.0, 5.0))
            await self.read_page(tab)
            return True

    def save(self, out_dir):
        out = list(map(lambda e: e.to_dict(), self.directory_entries))
        jason = json.dumps(out, indent=4)

        out_file = HERE.parent.parent / 'out' / (
                    '%s.pages%d-%d.json' % (self.newsgroup, self.start_page_num, self.current_page_num))

        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_dir / out_file, 'w') as f:
            f.write(jason)

        print('Saved %d entries to %s' % (len(out), str(out_file)))

    async def scrape(self, page_skip, page_limit, out_dir):
        async with Chrome() as browser:
            tab = await browser.start()
            await tab.go_to(self.search_url)
            await asyncio.sleep(2)
            await self.read_page(tab)
            self.current_page_num = 0
            more_pages = True
            while more_pages and (self.current_page_num < page_skip):
                more_pages = await self.next_page(tab)
                self.current_page_num += 1

            self.start_page_num = self.current_page_num
            if not more_pages:
                print('Skip too large, no pages included!')
                return

            while more_pages and (self.current_page_num < page_limit):
                self.add_page_entries()
                more_pages = await self.next_page(tab)
                self.current_page_num += 1

            self.save(out_dir)
