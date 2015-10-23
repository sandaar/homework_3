from string import punctuation
from collections import Counter
import argparse

from ascii_graph import Pyasciigraph


def load_file(filename):
    with open(filename, 'r') as f:
        text = f.read().lower()
    return text


def get_words(text):
    return [w.strip(punctuation) for w in text.split() if w.strip(punctuation)]


def get_letters(text):
    words = ''.join(get_words(text))
    letters = ([x for x in words if x.isalpha()])
    return letters


def count_letters(text):
    letters = get_letters(text)
    counted_letters = Counter(letters)
    return counted_letters


def visualize_data(counted_letters):
    data = counted_letters.items()
    graph = Pyasciigraph()
    for line in graph.graph('Frequency of letters', data):
        print(line)


def parse_args():
    parser = argparse.ArgumentParser(description='Letters frequency.')
    parser.add_argument('--filename', help='file name', required=True)
    args = vars(parser.parse_args())
    return args

if __name__ == '__main__':
    args = parse_args()
    filename = args['filename']
    text = load_file(filename)
    counted_letters = count_letters(text)
    visualize_data(counted_letters)
