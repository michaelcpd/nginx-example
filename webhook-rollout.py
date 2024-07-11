from flask import Flask, jsonify
import os
import sys
from kubernetes import client, config


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


def check_rollouts():
    config.load_kube_config()
    v1 = client.AppsV1Api()
    ret = v1.list_deployment_for_all_namespaces(watch=False)
    for i in ret.items:
        if i.status.updated_replicas != i.status.replicas:
            return True
    return False


@app.route('/check_rollout', methods=['GET'])
def check_rollout():
    if check_rollouts():
        return jsonify({"status": "rollout_in_progress"}), 409
    else:
        return jsonify({"status": "no_rollout_in_progress"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)