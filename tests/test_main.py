# tests/test_main.py

import pytest
from click.testing import CliRunner
from stresscli.main import cli

def test_main_dump_no_options():
    runner = CliRunner()
    result = runner.invoke(cli, ['dump'])
    assert result.exit_code == 0

def test_main_dump_with_options():
    runner = CliRunner()
    result = runner.invoke(cli, ['dump', '--config', 'config.yaml', '-o', 'output.yaml'])
    assert result.exit_code == 0
    assert 'Using configuration file: config.yaml' in result.output
    assert 'Output YAML file: output.yaml' in result.output

def test_main_test_no_options():
    runner = CliRunner()
    result = runner.invoke(cli, ['test'])
    assert result.exit_code == 0

def test_main_test_with_options():
    runner = CliRunner()
    result = runner.invoke(cli, ['test', '--dataset', 'dataset.csv', '--upload_to', 'report.txt', '-c', '10', '-d', '60'])
    assert result.exit_code == 0
    assert 'Using dataset: dataset.csv' in result.output
    assert 'Uploading final report to: report.txt' in result.output
    assert 'Concurrency level: 10' in result.output
    assert 'Test duration: 60' in result.output
