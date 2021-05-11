# pod から k8s へアクセスする

## 確認

```bash
# 環境変数
$ env
KUBERNETES_SERVICE_PORT=443
KUBERNETES_PORT=tcp://10.43.0.1:443
HOSTNAME=api-test-5b8547f7b6-5rr8r
SHLVL=2
HOME=/root
PKG_RELEASE=1
TERM=xterm-256color
NGINX_VERSION=1.19.10
KUBERNETES_PORT_443_TCP_ADDR=10.43.0.1
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
NJS_VERSION=0.5.3
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP=tcp://10.43.0.1:443
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_SERVICE_HOST=10.43.0.1
PWD=/

# Service AccountのToken
$ cat /var/run/secrets/kubernetes.io/serviceaccount/token ; echo ""

# ca.crt APIアクセスに必要な証明書
$ cat /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
-----END CERTIFICATE-----
```

## 環境変数の設定

```bash
$ TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
$ CACERT=var/run/secrets/kubernetes.io/serviceaccount/ca.crt
$ NAMESPACE="apitest"
$ k8s=$KUBERNETES_PORT_443_TCP_ADDR:$KUBERNETES_PORT_443_TCP_PORT
```

## アクセス確認

```bash
$ curl -H "Authorization: Bearer $TOKEN" --cacert $CACERT https://$k8s/healthz
ok
```

## API 経由のアクセス

```bash
$ vi deployment.json
{
    "kind": "Deployment",
    "apiVersion": "apps/v1",
    "metadata": {
        "name": "api-test-json",
        "namespace": "apitest",
        "labels": {
            "app": "api-test-json"
        }
    },
    "spec": {
        "replicas": 3,
        "selector": {
            "matchLabels": {
                "app": "api-test-json"
            }
        },
        "template": {
            "metadata": {
                "labels": {
                    "app": "api-test-json"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": "nginx-json",
                        "image": "nginx:alpine",
                        "resources": {}
                    }
                ]
            }
        },
        "strategy": {}
    }
}

$ curl -X POST -H "Authorization: Bearer $TOKEN" \
--cacert $CACERT -H "Content-Type:application/json" \
-d @deployment.json https://$k8s/apis/apps/v1/namespaces/apitest/deployments

{
  "kind": "Deployment",
  "apiVersion": "apps/v1",
  "metadata": {
    "name": "api-test-json",
    "namespace": "apitest",
    "uid": "3663daca-a612-4ab8-858c-ddd548d6354b",
    "resourceVersion": "307420",
    "generation": 1,
    "creationTimestamp": "2021-05-10T03:42:22Z",
    "labels": {
      "app": "api-test-json"
    },
    "managedFields": [
      {
        "manager": "curl",
        "operation": "Update",
        "apiVersion": "apps/v1",
        "time": "2021-05-10T03:42:22Z",
        "fieldsType": "FieldsV1",
        "fieldsV1": {"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{".":{},"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx-json\"}":{".":{},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}
      }
    ]
  },
  "spec": {
    "replicas": 3,
    "selector": {
      "matchLabels": {
        "app": "api-test-json"
      }
    },
    "template": {
      "metadata": {
        "creationTimestamp": null,
        "labels": {
          "app": "api-test-json"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "nginx-json",
            "image": "nginx:alpine",
            "resources": {

            },
            "terminationMessagePath": "/dev/termination-log",
            "terminationMessagePolicy": "File",
            "imagePullPolicy": "IfNotPresent"
          }
        ],
        "restartPolicy": "Always",
        "terminationGracePeriodSeconds": 30,
        "dnsPolicy": "ClusterFirst",
        "securityContext": {

        },
        "schedulerName": "default-scheduler"
      }
    },
    "strategy": {
      "type": "RollingUpdate",
      "rollingUpdate": {
        "maxUnavailable": "25%",
        "maxSurge": "25%"
      }
    },
    "revisionHistoryLimit": 10,
    "progressDeadlineSeconds": 600
  },
  "status": {

  }

# APIから確認
$ curl -X GET -H "Authorization: Bearer $TOKEN" --cacert $CACERT https://$k8s/apis/apps/v1/namespaces/apitest/deployments/api-test-json
{
  "kind": "Deployment",
  "apiVersion": "apps/v1",
  "metadata": {
    "name": "api-test-json",
    "namespace": "apitest",
    "uid": "3663daca-a612-4ab8-858c-ddd548d6354b",
    "resourceVersion": "307533",
    "generation": 1,
    "creationTimestamp": "2021-05-10T03:42:22Z",
    "labels": {
      "app": "api-test-json"
    },
    "annotations": {
      "deployment.kubernetes.io/revision": "1"
    },
    "managedFields": [
      {
        "manager": "curl",
        "operation": "Update",
        "apiVersion": "apps/v1",
        "time": "2021-05-10T03:42:22Z",
        "fieldsType": "FieldsV1",
        "fieldsV1": {"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{".":{},"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx-json\"}":{".":{},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}
      },
      {
        "manager": "k3s",
        "operation": "Update",
        "apiVersion": "apps/v1",
        "time": "2021-05-10T03:42:35Z",
        "fieldsType": "FieldsV1",
        "fieldsV1": {"f:metadata":{"f:annotations":{".":{},"f:deployment.kubernetes.io/revision":{}}},"f:status":{"f:availableReplicas":{},"f:conditions":{".":{},"k:{\"type\":\"Available\"}":{".":{},"f:lastTransitionTime":{},"f:lastUpdateTime":{},"f:message":{},"f:reason":{},"f:status":{},"f:type":{}},"k:{\"type\":\"Progressing\"}":{".":{},"f:lastTransitionTime":{},"f:lastUpdateTime":{},"f:message":{},"f:reason":{},"f:status":{},"f:type":{}}},"f:observedGeneration":{},"f:readyReplicas":{},"f:replicas":{},"f:updatedReplicas":{}}}
      }
    ]
  },
  "spec": {
    "replicas": 3,
    "selector": {
      "matchLabels": {
        "app": "api-test-json"
      }
    },
    "template": {
      "metadata": {
        "creationTimestamp": null,
        "labels": {
          "app": "api-test-json"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "nginx-json",
            "image": "nginx:alpine",
            "resources": {

            },
            "terminationMessagePath": "/dev/termination-log",
            "terminationMessagePolicy": "File",
            "imagePullPolicy": "IfNotPresent"
          }
        ],
        "restartPolicy": "Always",
        "terminationGracePeriodSeconds": 30,
        "dnsPolicy": "ClusterFirst",
        "securityContext": {

        },
        "schedulerName": "default-scheduler"
      }
    },
    "strategy": {
      "type": "RollingUpdate",
      "rollingUpdate": {
        "maxUnavailable": "25%",
        "maxSurge": "25%"
      }
    },
    "revisionHistoryLimit": 10,
    "progressDeadlineSeconds": 600
  },
  "status": {
    "observedGeneration": 1,
    "replicas": 3,
    "updatedReplicas": 3,
    "readyReplicas": 3,
    "availableReplicas": 3,
    "conditions": [
      {
        "type": "Available",
        "status": "True",
        "lastUpdateTime": "2021-05-10T03:42:35Z",
        "lastTransitionTime": "2021-05-10T03:42:35Z",
        "reason": "MinimumReplicasAvailable",
        "message": "Deployment has minimum availability."
      },
      {
        "type": "Progressing",
        "status": "True",
        "lastUpdateTime": "2021-05-10T03:42:35Z",
        "lastTransitionTime": "2021-05-10T03:42:22Z",
        "reason": "NewReplicaSetAvailable",
        "message": "ReplicaSet \"api-test-json-6f4b9b99d6\" has successfully progressed."
      }
    ]
  }

# 削除
$ curl -X DELETE -H "Authorization: Bearer $TOKEN" --cacert $CACERT https://$k8s/apis/apps/v1/namespaces/apitest/deployments/api-test-json
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {

  },
  "status": "Success",
  "details": {
    "name": "api-test-json",
    "group": "apps",
    "kind": "deployments",
    "uid": "3663daca-a612-4ab8-858c-ddd548d6354b"
  }
```
