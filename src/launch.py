from argparse import ArgumentParser
import asyncio
import sys

from pydoll.exceptions import NetworkError

from scraper.directory_scraper import DirectoryScraper

async def main():
    parser = ArgumentParser(prog='EGGS', description='Emergency Google Groups Scraper. Currently only gets post metadata')
    parser.add_argument('-n', '--newsgroup', help='newsgroup to scrape', required=True)
    parser.add_argument('-m', '--metadata-out', help='output directory for metadata files', required=True)
    parser.add_argument('-s', '--page-skip', help='skip to a specific page of results', type=int, default=0)
    parser.add_argument('-l', '--page-limit', help='stop after reaching a page number', type=int, default=999_999_999)
    args = parser.parse_args(args=(sys.argv[1:] or ['--help']))

    scrape = DirectoryScraper(newsgroup=args.newsgroup)
    try:
        await scrape.scrape(page_skip=args.page_skip, page_limit=args.page_limit, out_dir=args.out_dir)
    except (KeyboardInterrupt, NetworkError):
        scrape.save(out_dir=args.out_dir)
        sys.exit(130)


if __name__ == '__main__':
    asyncio.run(main())