import urlparse
import json
from collections import Counter

import argparse
import requests
from bs4 import BeautifulSoup


class Crawler(object):

    def __init__(self, root, size):
        self.root = root
        self.size = size
        self.queue = []
        self.followed = []
        self.data = {}

    def crawl(self):
        self.queue.append(self.root)

        while self.queue and len(self.data) < self.size:
            url = self.queue.pop()
            links = self.get_links(url)

            self.followed.append(url)

            counted_links = dict(Counter(links))
            for link, count in counted_links.items():
                self.add_data(link, url, count)

            for link in counted_links:
                if link not in self.followed:
                    self.queue.append(link)

    def save_data(self):
        with open('database.json', 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_data(self, link, url, count):
        if len(self.data) >= self.size:
            return None
        if link not in self.data:
            self.data[link] = {url: count}
        else:
            self.data[link][url] = count

    def get_links(self, url):
        soup = self.get_soup(url)
        root = self.get_url_root(url)
        links = self.retrieve_links(soup, root)
        return links

    def get_soup(self, url):
        try:
            response = requests.get(url)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                requests.exceptions.HTTPError,
                requests.exceptions.InvalidSchema) as e:
                print "Error: %s" % e
                return None
        status = response.status_code
        headers = response.headers["content-type"]
        if not is_response_ok(status) or not is_response_html(headers):
                return None
        encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding=encoding)
        return soup

    def get_url_root(self, url):
        parsed_url = urlparse.urlparse(url)
        scheme = parsed_url.scheme + '://'
        netloc = parsed_url.netloc
        root = scheme + netloc
        return root

    def retrieve_links(self, soup, root):
        links = []
        if not soup:
            return None
        for link in soup.find_all('a', href=True):
            relative_link = link.get('href')
            if not relative_link.startswith('http'):
                relative_link = urlparse.urljoin(root, relative_link)
            links.append(relative_link)
        return links


def is_response_ok(response_status_code):
    return response_status_code == requests.codes.ok


def is_response_html(response_headers):
    return response_headers == "text/html"


def parse_args():
    parser = argparse.ArgumentParser(description='Web crawler.')
    parser.add_argument('--url', help='initial url', required=True)
    parser.add_argument('--size', type=int, help='max size of database',
                        required=True)
    args = vars(parser.parse_args())
    return args

if __name__ == '__main__':
    args = parse_args()
    root = args['url']
    size = args['size']
    crawler = Crawler(root, size)
    crawler.crawl()
    crawler.save_data()
