# tests/test_dump.py

import pytest
from click.testing import CliRunner
from stresscli.dump import dump

def test_dump_no_options():
    runner = CliRunner()
    result = runner.invoke(dump)
    assert result.exit_code == 0

def test_dump_with_options():
    runner = CliRunner()
    result = runner.invoke(dump, ['--config', 'config.yaml', '-o', 'output.yaml'])
    assert result.exit_code == 0
    assert 'Using configuration file: config.yaml' in result.output
    assert 'Output YAML file: output.yaml' in result.output
