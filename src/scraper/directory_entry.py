import re
from datetime import datetime

from .selectors import DIRECTORY_SELECTORS

POST_AUTHOR = 'post_author'
POST_DATE = 'post_date'
POST_SUBJECT = 'post_subject'
POST_URL = 'post_url'
THREAD_ID = 'thread_id'
THREAD_TITLE = 'thread_title'

DATE_FORMAT = '%m/%d/%y'

THREAD_ID_REGEX = r'\./g/{newsgroup}/c/([a-zA-Z0-9-_]+)/m/.*'


class DirectoryEntry:
    def __init__(self, newsgroup, entry):
        self.entry = entry
        self.post_author = self.get_value(POST_AUTHOR)

        post_date_str = self.get_value(POST_DATE)

        self.post_date = datetime.strptime(post_date_str, DATE_FORMAT) if post_date_str else None

        self.post_subject = self.get_value(POST_SUBJECT)

        self.post_url = self.get_value(POST_URL, already_str=True)

        self.thread_title = self.get_value(THREAD_TITLE)

        if self.post_url:
            thread_id_match = re.search(THREAD_ID_REGEX.format(newsgroup=newsgroup), self.post_url)
            self.thread_id = thread_id_match.group(1) if thread_id_match else None
        else:
            self.thread_id = None

    def get_value(self, selector, already_str=False):
        vals = self.entry.xpath(DIRECTORY_SELECTORS[selector])
        if len(vals) > 0:
            return vals[0] if already_str else vals[0].text
        else:
            return None

    def to_dict(self):
        return {
            POST_AUTHOR: self.post_author,
            POST_DATE: self.post_date.strftime('%Y-%m-%d'),
            POST_SUBJECT: self.post_subject,
            POST_URL: self.post_url,
            THREAD_ID: self.thread_id,
            THREAD_TITLE: self.thread_title
        }
