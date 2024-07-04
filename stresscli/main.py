# stresscli/main.py

import click
from stresscli.dump import dump
from stresscli.load_test import load_test

@click.group()
@click.option('--kubeconfig', type=click.Path(), help='Configuration file to Kubernetes')
@click.option('--namespace', default='default', help='Namespace to dump Kubernetes config from')
def cli(kubeconfig,namespace):
    """StressCLI - A command line tool for stress testing OPEA workloads."""
    pass

cli.add_command(dump)
cli.add_command(load_test)

if __name__ == '__main__':
    cli()
