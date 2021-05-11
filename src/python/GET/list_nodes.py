from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()
ret = v1.list_node(watch=False)

for i in ret.items:
    print("{}\t{}\t{}".format(
        i.metadata.labels['kubernetes.io/hostname'],
        i.status.node_info.kubelet_version,
        i.status.node_info.kernel_version,
    ))
