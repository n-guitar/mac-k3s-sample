const k8s = require("@kubernetes/client-node");

const kc = new k8s.KubeConfig();
kc.loadFromDefault();

const k8sApi = kc.makeApiClient(k8s.CoreV1Api);

k8sApi.listNamespacedPod("default").then((res) => {
  for (let i in res.body.items) {
    console.log(res.body.items[i]);
  }
});
