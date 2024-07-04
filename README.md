# OPEAStress

This project includes benchmark toolset for AI workloads such as OPEA.

## stresscli

`stresscli` is a command line tool for dumping test specs and performing load tests.

### Prerequirements

This tool uses `wrk` to do load test. We need to install `wrk` and lua script packages.

```
sudo apt install wrk
sudo apt install luarocks lua-cjson
```

### Installation

The recommended way to install and run stresscli is in a virtualenv with the latest version of Python 3 (at least Python 3.11). If Python is not installed, you can likely install it using your distribution's
package manager, or see the [Python Download page](https://www.python.org/downloads/).

```bash
# create virtual env
python3 -m venv stresscli_virtualenv
source stresscli_virtualenv/bin/activate
# clone the project
git clone https://github.com/intel-sandbox/cloud.performance.benchmark.OPEAStress.git OPEAStress
cd OPEAStress
# install requirements
pip install -r requirements.txt
```

### Usage

#### Run a test

You can config the test profile in a yaml file and then run the load test. [run.yaml](./run.yaml) is a sample for your reference.

```
./stresscli.py load_test --profile run.yaml
```

#### Dump the configuration

You can dump the current testing profile by
```
./stresscli.py dump --kubeconfig <kubeconfig_file> -o <output_file>
```
