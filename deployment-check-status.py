import os
import sys


# Importa as bibliotecas necessárias para acessar a API do Kubernetes
from kubernetes import client, config

def check_rollouts():
    # Configura o acesso à API do Kubernetes
    config.load_kube_config()

    v1 = client.AppsV1Api()

    # Lista todas as implantações em todos os namespaces
    ret = v1.list_deployment_for_all_namespaces(watch=False)
    for i in ret.items:
        # Verifica se o rollout está em andamento
        if i.status.updated_replicas != i.status.replicas:
            print(f"Rollout in progress for deployment: {i.metadata.name}")
            return True

    return False

if __name__ == "__main__":
    if check_rollouts():
        sys.exit(1)
    else:
        sys.exit(0)