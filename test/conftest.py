import os
import json
import yaml

import pytest

INPUT_FILENAME = 'input.json'
OUTPUT_FILENAME = 'output.json'


@pytest.fixture(scope="module", autouse=True)
def input_data():
    filepath = os.path.dirname(__file__) + '/' + INPUT_FILENAME
    with open(filepath, 'r') as f:
        input_data = json.load(f)
    return input_data


@pytest.fixture(scope="module", autouse=True)
def output_data():
    filepath = os.path.dirname(__file__) + '/' + OUTPUT_FILENAME
    with open(filepath, 'r') as f:
        output_data = yaml.load(f)
    return output_data
