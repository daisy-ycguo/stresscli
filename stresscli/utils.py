# stresscli/utils.py

import yaml
import random
import string
from kubernetes import client, config as k8s_config

def dump_k8s_config(kubeconfig, output=None, return_as_dict=False, namespace='default'):
    """Dump the Kubernetes cluster configuration to a YAML file."""
    # Load Kubernetes configuration
    if kubeconfig:
        k8s_config.load_kube_config(config_file=kubeconfig)
    else:
        k8s_config.load_kube_config()

    # Initialize the Kubernetes API client
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()

    # Get all nodes in the cluster
    nodes = v1.list_node()
    node_deployments = {}

    #excluded_namespaces = {"kube-system", "kube-public", "kube-node-lease", "local-path-storage"}

    for node in nodes.items:
        node_name = node.metadata.name
        node_deployments[node_name] = {}

        # Get all pods running on the node
        field_selector = f'spec.nodeName={node_name}'
        #pods = v1.list_pod_for_all_namespaces(field_selector=field_selector)
        pods = v1.list_namespaced_pod(namespace=namespace, field_selector=field_selector)

        for pod in pods.items:
            #if pod.metadata.namespace in excluded_namespaces:
            #    continue
            owner_references = pod.metadata.owner_references
            for owner in owner_references:
                if owner.kind == 'ReplicaSet':
                    replicaset_name = owner.name
                    # Get the deployment owning the replicaset
                    rs = apps_v1.read_namespaced_replica_set(name=replicaset_name, namespace=pod.metadata.namespace)
                    for owner in rs.metadata.owner_references:
                        if owner.kind == 'Deployment':
                            deployment_name = owner.name
                            if deployment_name not in node_deployments[node_name]:
                                node_deployments[node_name][deployment_name] = {'replica': 0}
                            node_deployments[node_name][deployment_name]['replica'] += 1

    k8s_spec = {'workloadspec': node_deployments}

    if return_as_dict:
        return node_deployments
    else:
        # Write the deployment details to the YAML file
        with open(output, 'w') as yaml_file:
            yaml.dump(k8s_spec, yaml_file, default_flow_style=False)
        print(f'Cluster configuration written to {output}')

def generate_random_suffix(length=6):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_lua_script(template_path, output_path, dataset_path):
    """Generate a Lua script from the template with the specified dataset path."""
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
    
    script_content = template_content.replace("${DATASET_PATH}", dataset_path)
    
    with open(output_path, 'w') as output_file:
        output_file.write(script_content)