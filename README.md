# mac-k3s-sample

# crrate k3s

```bash
# run docker
$ K3S_TOKEN=${RANDOM}${RANDOM}${RANDOM} docker-compose up -d

# mac terminal
$ export KUBECONFIG=./kubeconfig.yaml
$ chmod 600 kubeconfig.yaml

# try kubectl
$ kubectl get nodes
NAME             STATUS   ROLES                  AGE   VERSION
k3s-controller   Ready    control-plane,master   53s   v1.20.5+k3s1
k3s-worker1      Ready    <none>                 45s   v1.20.5+k3s1
k3s-worker2      Ready    <none>                 45s   v1.20.5+k3s1

```

## wild card dns on docker container (option)

https://github.com/n-guitar/alpine-dnsmasq

```bash
$ cd dns
$ docker build -t dnsmasq:k3s.mac.domain .
$ docker run -d -p 53:53/tcp -p 53:53/udp --cap-add=NET_ADMIN \
-v $PWD/dnsmasq.conf:/etc/dnsmasq.conf \
--name dnsmasq dnsmasq:k3s.mac.domain
```

### bind error issue

https://github.com/docker/for-mac/issues/5335
https://matsuand.github.io/docs.docker.jp.onthefly/docker-for-mac/apple-m1/

### Docker Desktop RC 3

https://docs.docker.com/docker-for-mac/apple-m1/

## rancher with helm (option)

https://rancher.com/docs/rancher/v2.5/en/installation/install-rancher-on-k8s/

```bash
# Install the CustomResourceDefinition resources separately
$ kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v1.0.4/cert-manager.crds.yaml

# Create the namespace for cert-manager
$ kubectl create namespace cert-manager

# Add the Jetstack Helm repository
$ helm repo add jetstack https://charts.jetstack.io

# Update your local Helm chart repository cache
$ helm repo update

# Install the cert-manager Helm chart
$ helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --version v1.0.4

$ kubectl get pods --namespace cert-manager
NAME                                       READY   STATUS    RESTARTS   AGE
cert-manager-cainjector-55db655cd8-tkmct   1/1     Running   0          22s
cert-manager-6d87886d5c-94pxv              1/1     Running   0          22s
cert-manager-webhook-6846f844ff-8tj55      1/1     Running   0          22s


# add rancher

$ helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
$ kubectl create namespace cattle-system
$ helm install my-rancher rancher-stable/rancher --version 2.5.7 \
  --namespace cattle-system \
  --set hostname=rancher.k3s.mac.domain
```

## try curl (option)

https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/

```bash
$ kubectl config view -o jsonpath='{"Cluster name\tServer\n"}{range .clusters[*]}{.name}{"\t"}{.cluster.server}{"\n"}{end}'
Cluster name    Server
default https://127.0.0.1:6443

$ export CLUSTER_NAME="default"
$ APISERVER=$(kubectl config view -o jsonpath="{.clusters[?(@.name==\"$CLUSTER_NAME\")].cluster.server}")
$ TOKEN=$(kubectl get secrets -o jsonpath="{.items[?(@.metadata.annotations['kubernetes\.io/service-account\.name']=='default')].data.token}"|base64 --decode)

$ curl -X GET $APISERVER/api --header "Authorization: Bearer $TOKEN" --insecure
{
  "kind": "APIVersions",
  "versions": [
    "v1"
  ],
  "serverAddressByClientCIDRs": [
    {
      "clientCIDR": "0.0.0.0/0",
      "serverAddress": "172.23.0.4:6443"
    }
  ]
}
```

# python client

https://github.com/kubernetes-client/python

## setup python

```bash
$ python -m venv env
$ source ./env/bin/activate
$ pip install kubernetes
```

## sample

```bash
# pods all
$ python ./src/list_all_pods.py
```
