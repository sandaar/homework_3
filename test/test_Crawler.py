import ast
import json

import pytest

from crawler import Crawler

mark_crawler_tests = pytest.mark.regression


class TestCrawler(object):
    @mark_crawler_tests
    def test_get_links_positive(self, input_data, output_data):
        test_class = 'test_Crawler'
        test_name = 'test_get_links_positive'
        input_data = input_data[test_class][test_name]
        output_data = output_data[test_class][test_name]
        root = input_data['root']
        size = input_data['size']
        crawler = Crawler(root, size)
        links = crawler.get_links(root)
        assert links == output_data

    @mark_crawler_tests
    def test_get_links_negative(self, input_data, output_data):
        test_class = 'test_Crawler'
        test_name = 'test_get_links_negative'
        input_data = input_data[test_class][test_name]
        output_data = ast.literal_eval(output_data[test_class][test_name])
        root = input_data['root']
        size = input_data['size']
        crawler = Crawler(root, size)
        links = crawler.get_links(root)
        assert links == output_data

    @mark_crawler_tests
    def test_add_data_len_exceeds(self, input_data, output_data):
        test_class = 'test_Crawler'
        test_name = 'test_add_data_len_exceeds'
        input_data = input_data[test_class][test_name]
        output_data = ast.literal_eval(output_data[test_class][test_name])
        root = input_data['root']
        size = input_data['size']
        crawler = Crawler(root, size)
        result = crawler.add_data(root, root, 1)
        assert result == output_data

    @mark_crawler_tests
    def test_add_data_link_not_present(self, input_data, output_data):
        test_class = 'test_Crawler'
        test_name = 'test_add_data_link_not_present'
        input_data = input_data[test_class][test_name]
        output_data = output_data[test_class][test_name]
        root = input_data['root']
        size = input_data['size']
        url = input_data['url']
        crawler = Crawler(root, size)
        crawler.data = {root: {root: 1}}
        crawler.add_data(url, root, 1)
        assert crawler.data == output_data

    @mark_crawler_tests
    def test_add_data_link_present(self, input_data, output_data):
        test_class = 'test_Crawler'
        test_name = 'test_add_data_link_present'
        input_data = input_data[test_class][test_name]
        output_data = output_data[test_class][test_name]
        root = input_data['root']
        size = input_data['size']
        url = input_data['url']
        crawler = Crawler(root, size)
        crawler.data = {root: {root: 1}}
        crawler.add_data(root, url, 1)
        assert crawler.data == output_data

    @mark_crawler_tests
    def test_crawler(self, input_data, output_data):
        test_class = 'test_Crawler'
        test_name = 'test_crawler'
        input_data = input_data[test_class][test_name]
        output_data = output_data[test_class][test_name]
        root = input_data['root']
        size = int(input_data['size'])
        crawler = Crawler(root, size)
        crawler.crawl()
        crawler.save_data()
        with open('database.json', 'r') as f:
            actual_output = json.load(f)
        assert actual_output == output_data
