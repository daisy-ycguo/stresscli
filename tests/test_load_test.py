# tests/test_load_test.py

import pytest
from click.testing import CliRunner
from stresscli.load_test import load_test

def test_test_no_options():
    runner = CliRunner()
    result = runner.invoke(load_test)
    assert result.exit_code == 0

def test_test_with_options():
    runner = CliRunner()
    result = runner.invoke(load_test, ['--dataset', 'dataset.csv', '--upload_to', 'report.txt', '-c', '10', '-d', '60'])
    assert result.exit_code == 0
    assert 'Using dataset: dataset.csv' in result.output
    assert 'Uploading final report to: report.txt' in result.output
    assert 'Concurrency level: 10' in result.output
    assert 'Test duration: 60' in result.output
