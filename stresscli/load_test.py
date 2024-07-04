# stresscli/load_test.py

import os
import subprocess
import click
import yaml
from datetime import datetime
from .utils import dump_k8s_config
from .utils import generate_random_suffix, generate_lua_script

@click.command()
@click.option('--dataset', type=click.Path(), help='Dataset path')
@click.option('--endpoint', type=click.Path(), help='Endpoint of the test target service, like "http://192.168.0.12:8888/chatqna"')
@click.option('--profile', type=click.Path(), help='Path to profile YAML file')
@click.pass_context
#@click.option('--kubeconfig', type=click.Path(), help='Configuration file to Kubernetes')
def load_test(ctx, dataset, endpoint, profile):
    """Do load test"""
    kubeconfig = ctx.parent.params['kubeconfig']
    if dataset:
        click.echo(f'Using dataset: {dataset}')
    # Here you would add the logic to perform the load test
    if profile:
        with open(profile, 'r') as file:
            profile_data = yaml.safe_load(file)
        
        # Extract storage path and run details from profile
        hostpath = profile_data['profile']['storage']['hostpath']
        runs = profile_data['profile']['runs']
        
        for run in runs:
            run_name = run['name']
            namespace = run.get('namespace','default')
            loop = run.get('loop', 1)
            tool = run.get('tool', 'wrk')
            options = run['options']
            endpoint = run['endpoint']
            dataset = run.get('dataset', dataset)
            
            # Create the folder for the run
            random_suffix = generate_random_suffix()
            run_folder = os.path.join(hostpath, f"{run_name}_{random_suffix}")
            os.makedirs(run_folder, exist_ok=True)

            # Generate Lua script
            lua_template_path = "stresscli/lua_template/chatqna.template"
            lua_script_path = os.path.join(run_folder, "wrk_script.lua")
            generate_lua_script(lua_template_path, lua_script_path, dataset)   

            for i in range(loop):
                # Generate wrk command and execute it
                wrk_command = f'{tool} {options} --script {lua_script_path} {endpoint}'
                print(wrk_command)
                wrk_log_path = os.path.join(run_folder, f'wrk_{i + 1}.log')
                with open(wrk_log_path, 'w') as wrk_log:
                    subprocess.run(wrk_command.split(), stdout=wrk_log, stderr=subprocess.STDOUT)
                
                # Dump the k8s spec
                k8s_spec = dump_k8s_config(kubeconfig, return_as_dict=True, namespace=namespace)
                # Dump the test spec
                test_spec = {
                    'dataset': dataset,
                    'profile': profile,
                    'run': run,
                    'timestamp': datetime.now().isoformat()
                }
                # Combine both specs into a single YAML file
                combined_spec = {
                    'benchmarkspec': test_spec,
                    'workloadspec': k8s_spec
                }
                combined_spec_path = os.path.join(run_folder, f'testspec_{i + 1}.yaml')
                with open(combined_spec_path, 'w') as combined_file:
                    yaml.dump(combined_spec, combined_file)

        click.echo(f'Load test results saved to {run_folder}')
    else:
        click.echo('Profile is required to run the test.')
